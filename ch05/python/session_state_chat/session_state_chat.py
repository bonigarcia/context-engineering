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

import argparse
import os
import re
from dataclasses import dataclass, field
from typing import List

from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt


@dataclass
class SessionState:
    goal: str = ""
    stage: str = "collecting_context"
    topic: str = ""
    constraints: List[str] = field(default_factory=list)
    open_questions: List[str] = field(default_factory=list)
    turn_count: int = 0
    last_user_message: str = ""
    last_assistant_message: str = ""

    def render(self) -> str:
        lines = [
            f"goal: {self.goal or '(unset)'}",
            f"stage: {self.stage}",
            f"topic: {self.topic or '(unset)'}",
            f"turn_count: {self.turn_count}",
            f"constraints: {', '.join(self.constraints) if self.constraints else '(none)'}",
            f"open_questions: {', '.join(self.open_questions) if self.open_questions else '(none)'}",
            f"last_user_message: {self.last_user_message or '(unset)'}",
            f"last_assistant_message: {self.last_assistant_message or '(unset)'}",
        ]
        return "\n".join(f"- {line}" for line in lines)


def _extract_topic(text: str) -> str:
    words = re.findall(r"[A-Za-z][A-Za-z0-9_-]+", text)
    if not words:
        return ""
    return words[0].lower()


def _looks_like_new_goal(text: str) -> bool:
    lower = text.lower()
    return any(token in lower for token in ("instead", "switch to", "change to", "new task", "new goal", "actually"))


def update_state(state: SessionState, user_text: str, assistant_text: str) -> None:
    state.turn_count += 1
    state.last_user_message = user_text
    state.last_assistant_message = assistant_text

    if not state.goal.strip() or _looks_like_new_goal(user_text):
        state.goal = user_text.strip()
        state.topic = _extract_topic(user_text)
        state.constraints.clear()
        state.open_questions.clear()

    lower = user_text.lower()
    if any(token in lower for token in ("plan", "outline", "roadmap")):
        state.stage = "planning"
    elif any(token in lower for token in ("review", "check", "verify")):
        state.stage = "reviewing"
    elif any(token in lower for token in ("done", "finished", "complete")):
        state.stage = "done"
    else:
        state.stage = "working"

    if not state.topic.strip():
        state.topic = _extract_topic(user_text)

    constraint_match = re.search(r"(?:must|should|needs to|do not|don't)\s+([^.;!?]+)", user_text, re.IGNORECASE)
    if constraint_match:
        constraint = constraint_match.group(0).strip()
        if constraint not in state.constraints:
            state.constraints.append(constraint)
            state.constraints = state.constraints[-5:]

    if "?" in user_text:
        question = user_text.strip().rstrip("?")
        if question and question not in state.open_questions:
            state.open_questions.append(question)
            state.open_questions = state.open_questions[-5:]


def build_system_prompt(state: SessionState) -> str:
    return f"""You are a helpful assistant in a stateful demo.

The current session state is:
{state.render()}

Use the state as the current snapshot of the task. Keep answers concise and grounded in the
information already present in the session. If the user changes goals or constraints, adapt to the
new state instead of assuming older context is still correct.
""".strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Structured session state demo")
    parser.add_argument("--model", default=os.getenv("MODEL", "gpt-5"), help="OpenAI model")
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        Console().print("[bold red]OPENAI_API_KEY is not set.[/bold red] Put it in your environment or a .env file.")
        return 2

    console = Console()
    client = OpenAI()
    state = SessionState()
    transcript: List[dict[str, str]] = []

    console.print(f"[bold]Session state demo[/bold] model={args.model}")
    console.print("Type /help for commands.\n")

    help_text = (
        "Commands:\n"
        "  /help    show commands\n"
        "  /state   show the current session state\n"
        "  /reset   clear the session state\n"
        "  /exit    quit\n"
    )

    while True:
        try:
            user_text = Prompt.ask("[bold cyan]you[/bold cyan]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\nExiting.")
            return 0

        if not user_text:
            continue

        if user_text.startswith("/"):
            cmd = user_text.lower().strip()
            if cmd == "/help":
                console.print(help_text)
            elif cmd == "/state":
                console.print("[bold]Current session state[/bold]")
                console.print(state.render() + "\n")
            elif cmd == "/reset":
                state = SessionState()
                transcript.clear()
                console.print("Cleared session state.\n")
            elif cmd == "/exit":
                console.print("Goodbye.")
                return 0
            else:
                console.print("Unknown command. Type /help.\n")
            continue

        transcript.append({"role": "user", "content": user_text})
        system_prompt = build_system_prompt(state)
        response = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "system", "content": system_prompt}] + transcript
        )
        assistant_text = response.choices[0].message.content or ""
        transcript.append({"role": "assistant", "content": assistant_text})

        update_state(state, user_text, assistant_text)
        console.print(Markdown(assistant_text))
        console.print()


if __name__ == "__main__":
    raise SystemExit(main())
