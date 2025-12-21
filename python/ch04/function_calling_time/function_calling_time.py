#!/usr/bin/env python3
"""Function calling demo: 'What time is it in ...?'

This hands-on example accompanies Chapter 4 of *Context Engineering* and demonstrates
the core function-calling loop:

1) The model decides it needs external data
2) The app executes a deterministic function
3) The tool result is injected back as context
4) The model produces the final answer

Run:
  python function_calling_time.py
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt


_TIMEZONES = {
    "paris": "Europe/Paris",
    "new york": "America/New_York",
    "tokyo": "Asia/Tokyo",
    "london": "Europe/London",
    "sydney": "Australia/Sydney",
}

def get_current_time(city: str) -> str:
    """Return the current local time in a supported city."""
    tz = _TIMEZONES.get(city.strip().lower())
    if not tz:
        supported = ", ".join(sorted(_TIMEZONES.keys()))
        return f"Unknown city '{city}'. Supported cities: {supported}."
    now = datetime.now(ZoneInfo(tz))
    return now.strftime("%Y-%m-%d %H:%M:%S")


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current local time in a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (e.g., Paris, New York, Tokyo)",
                    }
                },
                "required": ["city"],
                "additionalProperties": False,
            },
        },
    }
]


def main() -> int:
    load_dotenv()
    console = Console()

    if not os.getenv("OPENAI_API_KEY"):
        console.print("[bold red]OPENAI_API_KEY is not set.[/bold red] Put it in your environment or a .env file.")
        return 2

    model = os.getenv("MODEL", "gpt-5")
    client = OpenAI()

    console.print(f"[bold]Function calling demo[/bold] model={model}")
    console.print("Ask about the current time in a city. Type /exit to quit.\n")

    messages: list[dict[str, object]] = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant.\n"
                "If you need the current time for a city, call the tool get_current_time.\n"
                "If the city is unsupported, ask the user to choose from the supported list."
            ),
        }
    ]

    while True:
        user_text = Prompt.ask("[bold cyan]you[/bold cyan]").strip()
        if not user_text:
            continue
        if user_text.lower() == "/exit":
            console.print("Goodbye.")
            return 0

        messages.append({"role": "user", "content": user_text})

        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.2,
        )

        msg = resp.choices[0].message
        messages.append(msg.model_dump())

        tool_calls = msg.tool_calls or []
        for call in tool_calls:
            if call.function.name != "get_current_time":
                tool_result = f"Unsupported tool: {call.function.name}"
            else:
                try:
                    args = json.loads(call.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                tool_result = get_current_time(city=str(args.get("city", "")))

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": tool_result,
                }
            )

        final = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="none",
            temperature=0.2,
        )

        assistant_text = (final.choices[0].message.content or "").strip()
        messages.append({"role": "assistant", "content": assistant_text})

        console.print(Markdown(assistant_text))
        console.print()

        if len(messages) > 30:
            messages = [messages[0]] + messages[-28:]

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
