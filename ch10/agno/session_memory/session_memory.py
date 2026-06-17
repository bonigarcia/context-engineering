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

from __future__ import annotations

from pathlib import Path

from agno.agent import Agent
from agno.db.json import JsonDb
from agno.models.openai import OpenAIResponses


def build_db(root: Path) -> JsonDb:
    return JsonDb(db_path=str(root / "session_memory.json"))


def build_agent(root: Path) -> Agent:
    return Agent(
        name="Session Memory",
        model=OpenAIResponses(id="gpt-5-mini"),
        db=build_db(root),
        session_id="chapter-session-memory",
        read_chat_history=True,
        add_history_to_context=True,
        store_history_messages=True,
        cache_session=True,
        markdown=True,
        instructions=(
            "Answer as if this is a continuing conversation. Use prior chat history when it "
            "exists, and point out that the session is persisted in a local JsonDb file."
        ),
    )


def main() -> None:
    root = Path(__file__).resolve().parent
    agent = build_agent(root)
    agent.print_response(
        "Tell me what you remember from our prior session, then continue the conversation.",
        stream=True,
    )


if __name__ == "__main__":
    main()
