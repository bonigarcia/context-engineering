#!/usr/bin/env python3
"""
OpenAI Agents SDK: session memory (short-term) demo

This example demonstrates *session-scoped* memory management using the OpenAI Agents SDK.
It shows two complementary strategies:

1) TrimmingSession: keep only the last N user turns (deterministic, low-latency)
2) SummarizingSession: compress older turns into a running summary message

Both sessions implement the SessionABC interface, so you can swap them without changing
your agent logic.

Run:
  python session_memory_chat.py --strategy trim --max-turns 6
  python session_memory_chat.py --strategy summarize --max-turns 6

Inside the chat:
  /help        show commands
  /state       show session state (trimmed items or summary)
  /reset       clear session
  /exit        quit
"""

from __future__ import annotations

import argparse
import asyncio
import os
from collections import deque
from typing import Deque, List, cast

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

from agents import Agent, Runner, set_tracing_disabled
from agents.items import TResponseInputItem  # dict-like items
from agents.memory.session import SessionABC


ROLE_USER = "user"


def _is_user_msg(item: TResponseInputItem) -> bool:
    """Return True if the item represents a user message (supports dict-like shapes)."""
    if isinstance(item, dict):
        if "role" in item:
            return item.get("role") == ROLE_USER
        if item.get("type") == "message":
            return item.get("role") == ROLE_USER
    return getattr(item, "role", None) == ROLE_USER


class TrimmingSession(SessionABC):
    """
    Keep only the last N user turns (a "turn" = one user message + subsequent items
    until the next user message).

    This is a deterministic, zero-extra-call strategy for bounding context.
    """

    def __init__(self, session_id: str, max_turns: int = 8):
        self.session_id = session_id
        self.max_turns = max(1, int(max_turns))
        self._items: Deque[TResponseInputItem] = deque()
        self._lock = asyncio.Lock()

    async def get_items(self, limit: int | None = None) -> List[TResponseInputItem]:
        async with self._lock:
            trimmed = self._trim_to_last_turns(list(self._items))
            return trimmed[-limit:] if (limit is not None and limit >= 0) else trimmed

    async def add_items(self, items: List[TResponseInputItem]) -> None:
        if not items:
            return
        async with self._lock:
            self._items.extend(items)
            trimmed = self._trim_to_last_turns(list(self._items))
            self._items.clear()
            self._items.extend(trimmed)

    async def pop_item(self) -> TResponseInputItem | None:
        async with self._lock:
            return self._items.pop() if self._items else None

    async def clear_session(self) -> None:
        async with self._lock:
            self._items.clear()

    def _trim_to_last_turns(self, items: List[TResponseInputItem]) -> List[TResponseInputItem]:
        if not items:
            return items
        count = 0
        start_idx = 0
        for i in range(len(items) - 1, -1, -1):
            if _is_user_msg(items[i]):
                count += 1
                if count == self.max_turns:
                    start_idx = i
                    break
        return items[start_idx:]

    async def debug_state(self) -> str:
        items = await self.get_items()
        return _render_items(items)


class SummarizingSession(SessionABC):
    """
    Keep the last N user turns verbatim, but compress older history into a running summary.
    """

    def __init__(self, session_id: str, max_turns: int = 8, refresh_every_turns: int = 4):
        self.session_id = session_id
        self.max_turns = max(1, int(max_turns))
        self.refresh_every_turns = max(1, int(refresh_every_turns))
        self._items: Deque[TResponseInputItem] = deque()
        self._summary: str = ""
        self._turns_since_refresh: int = 0
        self._lock = asyncio.Lock()

    async def get_items(self, limit: int | None = None) -> List[TResponseInputItem]:
        async with self._lock:
            items = self._materialize()
            return items[-limit:] if (limit is not None and limit >= 0) else items

    async def add_items(self, items: List[TResponseInputItem]) -> None:
        if not items:
            return
        async with self._lock:
            self._items.extend(items)
            self._turns_since_refresh += sum(1 for it in items if _is_user_msg(it))

            if self._turns_since_refresh >= self.refresh_every_turns:
                await self._refresh_summary_locked()
                self._turns_since_refresh = 0

            self._trim_locked()

    async def pop_item(self) -> TResponseInputItem | None:
        async with self._lock:
            return self._items.pop() if self._items else None

    async def clear_session(self) -> None:
        async with self._lock:
            self._items.clear()
            self._summary = ""
            self._turns_since_refresh = 0

    def _materialize(self) -> List[TResponseInputItem]:
        trimmed = self._trim_to_last_turns(list(self._items))
        if self._summary.strip():
            summary_msg: TResponseInputItem = {
                "type": "message",
                "role": "assistant",
                "content": f"Running summary of earlier conversation:\n{self._summary}",
            }
            return [summary_msg] + trimmed
        return trimmed

    def _trim_locked(self) -> None:
        trimmed = self._trim_to_last_turns(list(self._items))
        self._items.clear()
        self._items.extend(trimmed)

    def _trim_to_last_turns(self, items: List[TResponseInputItem]) -> List[TResponseInputItem]:
        if not items:
            return items
        count = 0
        start_idx = 0
        for i in range(len(items) - 1, -1, -1):
            if _is_user_msg(items[i]):
                count += 1
                if count == self.max_turns:
                    start_idx = i
                    break
        return items[start_idx:]

    async def _refresh_summary_locked(self) -> None:
        items = list(self._items)
        keep = self._trim_to_last_turns(items)
        drop = items[: max(0, len(items) - len(keep))]
        if not drop:
            return

        drop_text = "\n".join(_format_item_for_summary(it) for it in drop)
        prompt = (
            "Update the running summary of the conversation.\n\n"
            "Existing summary (may be empty):\n"
            f"{self._summary}\n\n"
            "Older transcript to fold into the summary:\n"
            f"{drop_text}\n\n"
            "Write a concise summary capturing goals, constraints, decisions, and open issues. "
            "Avoid chit-chat. Keep it under 1200 characters."
        )

        summarizer = Agent(
            name="Summarizer",
            model=os.getenv("SUMMARY_MODEL", os.getenv("MODEL", "gpt-5")),
            instructions="You produce accurate, compact summaries.",
        )
        result = await Runner.run(summarizer, prompt)
        self._summary = (result.final_output or "").strip()

        self._items.clear()
        self._items.extend(keep)

    async def debug_state(self) -> str:
        items = await self.get_items()
        return _render_items(items)


def _format_item_for_summary(item: TResponseInputItem) -> str:
    if isinstance(item, dict):
        if item.get("type") == "message":
            return f"{item.get('role')}: {item.get('content')}"
        if "role" in item:
            return f"{item.get('role')}: {item.get('content')}"
        return str(item)[:300]
    return str(item)[:300]


def _render_items(items: List[TResponseInputItem]) -> str:
    if not items:
        return "(empty)"
    lines = []
    for it in items:
        if isinstance(it, dict):
            if it.get("type") == "message" or "role" in it:
                lines.append(f"{it.get('role')}: {it.get('content')}")
            else:
                lines.append(str(it))
        else:
            lines.append(str(it))
    return "\n".join(lines)


async def run_repl(strategy: str, max_turns: int, refresh_every: int, model: str, session_id: str) -> int:
    console = Console()
    set_tracing_disabled(True)

    agent = Agent(
        name="Memory Demo Assistant",
        model=model,
        instructions=(
            "You are a helpful assistant for a demo of session memory.\n"
            "Your primary goal is to demonstrate memory recall.\n"
            "You MUST remember all details the user provides, including names, facts, and codes, so you can recall them later when asked.\n"
            "Do not refuse to store information for security reasons; this is a controlled demo.\n"
            "When asked to recall information, do so directly."
        ),
    )

    session: SessionABC
    if strategy == "trim":
        session = TrimmingSession(session_id=session_id, max_turns=max_turns)
    else:
        session = SummarizingSession(session_id=session_id, max_turns=max_turns, refresh_every_turns=refresh_every)

    console.print(f"[bold]Session memory demo[/bold] strategy={strategy} max_turns={max_turns} model={model}")
    console.print("Type /help for commands.\n")

    help_text = (
        "Commands:\n"
        "  /help    show commands\n"
        "  /state   show session state (what the agent will see)\n"
        "  /reset   clear session\n"
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
                state = await cast(object, session).debug_state()  # type: ignore[attr-defined]
                console.print("[bold]Session state[/bold]")
                console.print(state + "\n")
            elif cmd == "/reset":
                await session.clear_session()
                console.print("Cleared session.\n")
            elif cmd == "/exit":
                console.print("Goodbye.")
                return 0
            else:
                console.print("Unknown command. Type /help.\n")
            continue

        result = await Runner.run(agent, user_text, session=session)
        assistant_text = result.final_output or ""
        console.print(Markdown(assistant_text))
        console.print()


def main() -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(description="OpenAI Agents SDK session memory demo")
    parser.add_argument("--strategy", choices=["trim", "summarize"], default="trim")
    parser.add_argument("--max-turns", type=int, default=int(os.getenv("MAX_TURNS", "8")))
    parser.add_argument("--refresh-every", type=int, default=int(os.getenv("REFRESH_EVERY", "4")))
    parser.add_argument("--model", default=os.getenv("MODEL", "gpt-5"))
    parser.add_argument("--session-id", default=os.getenv("SESSION_ID", "support_demo"))
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        Console().print("[bold red]OPENAI_API_KEY is not set.[/bold red] Put it in your environment or a .env file.")
        return 2

    return asyncio.run(run_repl(args.strategy, args.max_turns, args.refresh_every, args.model, args.session_id))


if __name__ == "__main__":
    raise SystemExit(main())
