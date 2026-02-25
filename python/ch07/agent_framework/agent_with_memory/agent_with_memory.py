import asyncio
from collections.abc import MutableSequence, Sequence
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel

from agent_framework import Agent, Context, ContextProvider, ChatOptions
from agent_framework.openai import OpenAIChatClient


MODEL_ID = "gpt-4o-mini"

try:
    from agent_framework import Message
except Exception:
    from agent_framework import ChatMessage as Message

class UserInfo(BaseModel):
    name: str | None = None
    age: int | None = None


class UserInfoMemory(ContextProvider):
    def __init__(self, chat_client: Any, user_info: UserInfo | None = None, **kwargs: Any):
        self._chat_client = chat_client
        if user_info is not None:
            self.user_info = user_info
        elif kwargs:
            self.user_info = UserInfo.model_validate(kwargs)
        else:
            self.user_info = UserInfo()

    async def invoked(
            self,
            request_messages: Message | Sequence[Message],
            response_messages: Message | Sequence[Message] | None = None,
            invoke_exception: Exception | None = None,
            **kwargs: Any,
    ) -> None:
        messages_list = [request_messages] if isinstance(request_messages, Message) else list(request_messages)

        user_msgs = [
            m for m in messages_list
            if getattr(getattr(m, "role", None), "value", getattr(m, "role", None)) == "user"
        ]

        if (self.user_info.name is None or self.user_info.age is None) and user_msgs:
            try:
                result = await self._chat_client.get_response(
                    messages=messages_list,
                    chat_options=ChatOptions(
                        instructions=(
                            "Extract the user's name and age from the message. "
                            "Return nulls if not present."
                        ),
                        response_format=UserInfo,
                    ),
                )

                value = getattr(result, "value", None) or result
                if isinstance(value, UserInfo):
                    if self.user_info.name is None and value.name:
                        self.user_info.name = value.name
                    if self.user_info.age is None and value.age is not None:
                        self.user_info.age = value.age
            except Exception:
                pass

    async def invoking(self, messages: Message | MutableSequence[Message], **kwargs: Any) -> Context:
        instructions: list[str] = []

        if self.user_info.name is None:
            instructions.append(
                "Ask the user for their name and refuse to answer questions until they provide it."
            )
        else:
            instructions.append(f"The user's name is {self.user_info.name}.")

        if self.user_info.age is None:
            instructions.append(
                "Ask the user for their age and refuse to answer questions until they provide it."
            )
        else:
            instructions.append(f"The user's age is {self.user_info.age}.")

        return Context(instructions=" ".join(instructions))

    def serialize(self) -> str:
        return self.user_info.model_dump_json()


def _extract_userinfo_memory(ctx_provider: Any) -> UserInfoMemory | None:
    """
    Agent Framework versions differ:
    - sometimes thread.context_provider is the provider itself
    - sometimes it's a composite with .providers
    """
    if isinstance(ctx_provider, UserInfoMemory):
        return ctx_provider

    providers = getattr(ctx_provider, "providers", None)
    if providers:
        for p in providers:
            if isinstance(p, UserInfoMemory):
                return p

    return None


async def main() -> None:
    load_dotenv()

    chat_client = OpenAIChatClient(model_id=MODEL_ID)
    memory_provider = UserInfoMemory(chat_client)

    async with Agent(
            client=chat_client,
            instructions="You are a friendly assistant. Always address the user by name.",
            context_provider=memory_provider,
    ) as agent:

        thread = agent.get_new_thread()

        print("\nAgent ready. Type 'exit' to quit.\n")
        print("Try asking a question first — it should request name/age.\n")

        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit"}:
                break

            reply = await agent.run(user_input, thread=thread)
            print(f"\nAgent: {reply}\n")

            # Robust debug memory display
            mem = _extract_userinfo_memory(getattr(thread, "context_provider", None))

if __name__ == "__main__":
    asyncio.run(main())
