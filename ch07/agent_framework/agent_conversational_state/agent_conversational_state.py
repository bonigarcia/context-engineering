import asyncio
import json
import re
from collections.abc import MutableSequence, Sequence
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from agent_framework import Agent, Context, ContextProvider
from agent_framework.openai import OpenAIChatClient


MODEL_ID = "gpt-4o-mini"
STATE_FILE = Path("conversation_state.json")

try:
    from agent_framework import Message  # type: ignore
except Exception:
    from agent_framework import ChatMessage as Message  # type: ignore


class ConversationState(BaseModel):
    goal: str | None = None
    plan: list[str] = Field(default_factory=list)
    current_step_index: int = 0
    completed_steps: list[str] = Field(default_factory=list)

    def reset_progress(self) -> None:
        self.plan = []
        self.current_step_index = 0
        self.completed_steps = []

    def current_step(self) -> str | None:
        if 0 <= self.current_step_index < len(self.plan):
            return self.plan[self.current_step_index]
        return None

    def remaining_steps(self) -> list[str]:
        if self.current_step_index < len(self.plan):
            return self.plan[self.current_step_index :]
        return []

    def advance(self) -> bool:
        """Mark current step complete and advance. Returns True if advanced."""
        step = self.current_step()
        if step is None:
            return False
        self.completed_steps.append(step)
        self.current_step_index += 1
        return True


def _role_value(msg: Any) -> str | None:
    role = getattr(msg, "role", None)
    if role is None:
        return None
    return getattr(role, "value", role)


def _text_value(msg: Any) -> str:
    for attr in ("content", "text", "value"):
        v = getattr(msg, attr, None)
        if isinstance(v, str) and v.strip():
            return v
    v = getattr(msg, "content", None)
    return str(v) if v is not None else ""


class ConversationalStateProvider(ContextProvider):
    """
    Conversational "state" implemented as a ContextProvider.

    - invoking(): injects current state into model context before inference
    - invoked(): updates state after each turn based on user commands / text
    - serialize(): allows persistence of state across restarts
    """

    def __init__(self, state: ConversationState | None = None, **kwargs: Any):
        if state is not None:
            self.state = state
        elif kwargs:
            self.state = ConversationState.model_validate(kwargs)
        else:
            self.state = ConversationState()

    async def invoking(self, messages: Message | MutableSequence[Message], **kwargs: Any) -> Context:
        s = self.state

        if not s.goal:
            return Context(
                instructions=(
                    "You are a goal-driven assistant.\n"
                    "The user has NOT set a goal yet.\n"
                    "Ask for a goal before answering anything else. Politely refuse to proceed until a goal is provided.\n"
                    "Example: 'What is your goal? You can say: /goal <text>'."
                )
            )

        # If goal exists, inject the state as operational context
        plan_text = "\n".join([f"- {p}" for p in s.plan]) if s.plan else "(no plan set)"
        completed_text = "\n".join([f"- {c}" for c in s.completed_steps]) if s.completed_steps else "(none)"
        current = s.current_step() or "(no current step)"

        return Context(
            instructions=(
                "You are a goal-driven assistant.\n"
                "Use the following STATE to keep continuity and avoid re-asking for known info.\n"
                f"GOAL: {s.goal}\n"
                f"PLAN:\n{plan_text}\n"
                f"CURRENT STEP INDEX: {s.current_step_index}\n"
                f"CURRENT STEP: {current}\n"
                f"COMPLETED STEPS:\n{completed_text}\n"
                "If the user asks 'what next', point to the current step.\n"
                "If no plan exists, propose a short 3–5 step plan and ask the user to confirm.\n"
                "Do not invent completed work; only use the state."
            )
        )

    async def invoked(
            self,
            request_messages: Message | Sequence[Message],
            response_messages: Message | Sequence[Message] | None = None,
            invoke_exception: Exception | None = None,
            **kwargs: Any,
    ) -> None:
        # Update state based on the last user message
        msgs = [request_messages] if isinstance(request_messages, Message) else list(request_messages)
        user_msgs = [m for m in msgs if _role_value(m) == "user"]
        if not user_msgs:
            return

        text = _text_value(user_msgs[-1]).strip()
        if not text:
            return

        s = self.state

        # Commands
        if text.lower().startswith("/reset"):
            s.goal = None
            s.reset_progress()
            return

        if text.lower().startswith("/goal "):
            s.goal = text[6:].strip() or None
            s.reset_progress()
            return

        if text.lower().startswith("/plan "):
            raw = text[6:].strip()
            steps = [p.strip() for p in raw.split("|") if p.strip()]
            s.plan = steps
            s.current_step_index = 0
            s.completed_steps = []
            return

        if text.lower().startswith("/next"):
            s.advance()
            return

        # Natural language: "my goal is ..."
        m_goal = re.search(r"\bmy goal is\s+(?P<goal>.+)$", text, re.IGNORECASE)
        if m_goal and not s.goal:
            s.goal = m_goal.group("goal").strip()
            s.reset_progress()
            return

        # Natural language: "I completed <something>"
        m_done = re.search(r"\b(i completed|i finished|done with)\s+(?P<done>.+)$", text, re.IGNORECASE)
        if m_done and s.goal:
            done = m_done.group("done").strip().rstrip(".")
            # If this matches the current step, advance; otherwise record it as completed note
            cur = s.current_step()
            if cur and done.lower() in cur.lower():
                s.advance()
            else:
                s.completed_steps.append(done)

    def serialize(self) -> str:
        return self.state.model_dump_json()


def load_state() -> ConversationState:
    if not STATE_FILE.exists():
        return ConversationState()
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        return ConversationState.model_validate(data)
    except Exception:
        return ConversationState()


def save_state(state: ConversationState) -> None:
    STATE_FILE.write_text(state.model_dump_json(indent=2), encoding="utf-8")


async def main() -> None:
    load_dotenv()

    client = OpenAIChatClient(model_id=MODEL_ID)

    state = load_state()
    provider = ConversationalStateProvider(state=state)

    async with Agent(
            client=client,
            instructions=(
                    "You are a helpful assistant. Be concise.\n"
                    "The system may provide you with STATE. Follow it."
            ),
            context_provider=provider,
    ) as agent:
        thread = agent.get_new_thread()

        print("\nStateful agent ready. Type 'exit' to quit.\n")
        print("Commands: /goal, /plan, /next, /state, /reset\n")

        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit"}:
                break

            if user_input.lower().startswith("/state"):
                print("\n(state file snapshot)")
                print(provider.state.model_dump_json(indent=2))
                print()
                continue

            reply = await agent.run(user_input, thread=thread)
            print(f"\nAgent: {reply}\n")

            # persist after each turn
            save_state(provider.state)

    # persist on exit too
    save_state(provider.state)


if __name__ == "__main__":
    asyncio.run(main())
