"""
(C) Copyright 2026 Boni Garcia (https://bonigarcia.github.io/)
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import asyncio
from collections.abc import MutableSequence, Sequence
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel

from agent_framework import Agent, ChatOptions, ContextProvider, SessionContext
from agent_framework.openai import OpenAIChatClient


MODEL_ID = "gpt-5-mini"

try:
    from agent_framework import Message
except Exception:
    from agent_framework import ChatMessage as Message

class UserInfo(BaseModel):
    name: str | None = None
    age: int | None = None


class UserInfoMemory(ContextProvider):
    def __init__(self, chat_client: Any, user_info: UserInfo | None = None, **kwargs: Any):
        super().__init__(source_id="user-info-memory")
        self._chat_client = chat_client
        if user_info is not None:
            self.user_info = user_info
        elif kwargs:
            self.user_info = UserInfo.model_validate(kwargs)
        else:
            self.user_info = UserInfo()

    async def after_run(
            self,
            *,
            agent: Any,
            session: Any,
            context: SessionContext,
            state: dict[str, Any],
            **kwargs: Any,
    ) -> None:
        user_msgs = [
            m for m in context.input_messages
            if getattr(getattr(m, "role", None), "value", getattr(m, "role", None)) == "user"
        ]

        if (self.user_info.name is None or self.user_info.age is None) and user_msgs:
            try:
                messages_list = context.input_messages
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

    async def before_run(
            self,
            *,
            agent: Any,
            session: Any,
            context: SessionContext,
            state: dict[str, Any],
            **kwargs: Any,
    ) -> None:
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

        context.extend_instructions(self.source_id, " ".join(instructions))

def serialize(self) -> str:
    return self.user_info.model_dump_json()


async def main() -> None:
    load_dotenv()

    chat_client = OpenAIChatClient(model=MODEL_ID)
    memory_provider = UserInfoMemory(chat_client)

    async with Agent(
            client=chat_client,
            instructions="You are a friendly assistant. Always address the user by name.",
            context_providers=[memory_provider],
    ) as agent:
        session = agent.create_session()

        print("\nAgent ready. Type 'exit' to quit.\n")
        print("Try asking a question first — it should request name/age.\n")

        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit"}:
                break

            reply = await agent.run(user_input, session=session)
            print(f"\nAgent: {reply}\n")

if __name__ == "__main__":
    asyncio.run(main())
