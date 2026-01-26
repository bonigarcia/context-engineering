import os
import uuid
from dotenv import load_dotenv

from langchain_classic import hub
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun

# ----------------------------
# Langfuse imports (SDK versions vary)
# ----------------------------
try:
    # Recommended in newer SDKs
    from langfuse import get_client
except Exception:
    get_client = None  # fallback below

try:
    # Langfuse v3+ (current)
    from langfuse.langchain import CallbackHandler
except ModuleNotFoundError:
    # Langfuse v2.x (legacy)
    from langfuse.callback import CallbackHandler

# ----------------------------
# Agent API compatibility:
# Prefer LangChain v1 create_agent; fall back to classic create_react_agent + AgentExecutor.
# ----------------------------
try:
    from langchain.agents import create_agent  # LangChain v1+
    AGENT_MODE = "v1"
except ImportError:
    from langchain.agents import create_react_agent  # classic
    AGENT_MODE = "classic"

    # Classic AgentExecutor import paths vary by version
    try:
        from langchain.agents.agent import AgentExecutor  # older-ish
    except Exception:
        from langchain.agents import AgentExecutor  # older


def _ensure_env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise ValueError(f"{name} must be set (environment or .env).")
    return val


def _get_langfuse_client():
    """
    Return a Langfuse client object if available (preferred), else None.
    We avoid relying on handler methods like get_trace_url(), which may not exist.
    """
    if get_client is None:
        return None
    try:
        return get_client()
    except Exception:
        return None


def _invoke_with_callbacks(obj, payload, callbacks, trace_id: str, *, is_v1: bool):
    """
    Invoke an agent/chain across versions:
    - v1 agents typically accept invoke(payload, config={...})
    - classic AgentExecutor often accepts invoke(payload, config_dict) (2nd positional arg)
    """
    config = {"callbacks": callbacks, "run_id": trace_id}

    if is_v1:
        # Most v1: invoke(payload, config={...})
        try:
            return obj.invoke(payload, config=config)
        except TypeError:
            # Some variants accept positional config
            return obj.invoke(payload, config)
    else:
        # Classic AgentExecutor: invoke(payload, config_dict) is common
        try:
            return obj.invoke(payload, config)
        except TypeError:
            # Some variants use invoke(payload) only; fallback without run_id propagation
            # (still traces via callbacks, but URL may not be derivable deterministically)
            return obj.invoke(payload)


def main():
    load_dotenv()

    _ensure_env("OPENAI_API_KEY")
    _ensure_env("LANGFUSE_PUBLIC_KEY")
    _ensure_env("LANGFUSE_SECRET_KEY")
    # LANGFUSE_HOST is optional (defaults depend on SDK); set it if you use self-hosted.

    # Langfuse client (for URL construction)
    langfuse_client = _get_langfuse_client()

    # LLM + tools
    llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
    tools = [DuckDuckGoSearchRun()]

    # Langfuse callback handler (LangChain integration)
    langfuse_handler = CallbackHandler()

    print("--- Running agent with Langfuse tracing ---")
    question = "What was the score of the last Super Bowl and who won?"

    # Use a deterministic trace id by forcing LangChain run_id
    trace_id = str(uuid.uuid4())

    if AGENT_MODE == "v1":
        system_prompt = (
            "You are a helpful assistant. Use tools when needed to answer questions. "
            "When you have the final answer, respond concisely."
        )
        agent = create_agent(model=llm, tools=tools, system_prompt=system_prompt)

        response = _invoke_with_callbacks(
            agent,
            {"messages": [{"role": "user", "content": question}]},
            callbacks=[langfuse_handler],
            trace_id=trace_id,
            is_v1=True,
        )

        # Extract final answer from common response shapes
        final_answer = None
        if isinstance(response, dict) and "messages" in response and response["messages"]:
            # try to find last assistant message
            for msg in reversed(response["messages"]):
                if isinstance(msg, dict) and msg.get("role") == "assistant":
                    final_answer = msg.get("content")
                    break
            if final_answer is None:
                last = response["messages"][-1]
                final_answer = last.get("content") if isinstance(last, dict) else str(last)
        else:
            final_answer = str(response)

    else:
        # Classic ReAct agent via hub
        prompt = hub.pull("hwchase17/react")
        agent = create_react_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        response = _invoke_with_callbacks(
            agent_executor,
            {"input": question},
            callbacks=[langfuse_handler],
            trace_id=trace_id,
            is_v1=False,
        )
        if isinstance(response, dict):
            final_answer = response.get("output") or response.get("final") or str(response)
        else:
            final_answer = str(response)

    # Trace URL (do not rely on handler.get_trace_url(), which may not exist)
    print("\n--- Trace ---")
    if langfuse_client is not None:
        try:
            trace_url = langfuse_client.get_trace_url(trace_id=trace_id)
            print(f"View the trace in Langfuse: {trace_url}")
        except Exception:
            print(f"Trace created; trace_id={trace_id} (URL unavailable from client in this SDK).")
    else:
        print(f"Trace created; trace_id={trace_id} (install/upgrade langfuse to enable get_trace_url).")

    print("\n--- Final Answer ---")
    print(final_answer)


if __name__ == "__main__":
    main()