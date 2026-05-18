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
import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List

from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt


@dataclass
class WorkflowState:
    objective: str = ""
    status: str = "idle"
    current_step: int = 0
    plan: List[str] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    planner_notes: str = ""
    executor_notes: str = ""
    turn_count: int = 0
    handoff_log: List[str] = field(default_factory=list)

    def render(self) -> str:
        lines = [
            f"objective: {self.objective or '(unset)'}",
            f"status: {self.status}",
            f"current_step: {self.current_step}",
            f"plan: {self.plan if self.plan else '(none)'}",
            f"blockers: {self.blockers if self.blockers else '(none)'}",
            f"planner_notes: {self.planner_notes or '(none)'}",
            f"executor_notes: {self.executor_notes or '(none)'}",
            f"turn_count: {self.turn_count}",
            f"handoff_log: {self.handoff_log[-4:] if self.handoff_log else '(none)'}",
        ]
        return "\n".join(f"- {line}" for line in lines)


def load_state(path: Path) -> WorkflowState:
    if not path.exists():
        return WorkflowState()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return WorkflowState()
    return WorkflowState(
        objective=str(data.get("objective", "")),
        status=str(data.get("status", "idle")),
        current_step=int(data.get("current_step", 0)),
        plan=[str(item) for item in data.get("plan", []) if str(item).strip()],
        blockers=[str(item) for item in data.get("blockers", []) if str(item).strip()],
        planner_notes=str(data.get("planner_notes", "")),
        executor_notes=str(data.get("executor_notes", "")),
        turn_count=int(data.get("turn_count", 0)),
        handoff_log=[str(item) for item in data.get("handoff_log", []) if str(item).strip()],
    )


def save_state(path: Path, state: WorkflowState) -> None:
    path.write_text(json.dumps(asdict(state), indent=2), encoding="utf-8")


def _ensure_list(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def request_json(client: OpenAI, model: str, instructions: str, prompt: str) -> Dict[str, Any]:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )
    raw = response.choices[0].message.content or "{}"
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = {"raw": raw}
    return parsed if isinstance(parsed, dict) else {"raw": raw}


def build_planner_prompt(state: WorkflowState, user_request: str) -> str:
    return f"""Shared workflow state:
{state.render()}

User request:
{user_request}

Return JSON with these keys:
- objective: concise statement of the current goal
- plan: ordered list of 3 to 5 short steps
- handoff_note: short note for the executor agent
- risks: list of likely blockers or assumptions
""".strip()


def build_executor_prompt(state: WorkflowState) -> str:
    return f"""You are the executor agent in a two-agent workflow.

Read the shared workflow state carefully and continue from the current plan.

Shared workflow state:
{state.render()}

Return JSON with these keys:
- status: one of idle, planned, in_progress, blocked, or complete
- completed_step: short description of the step just completed
- blockers: list of unresolved blockers
- next_step: short description of the next step to take
""".strip()


def apply_planner_result(state: WorkflowState, payload: Dict[str, Any]) -> None:
    objective = str(payload.get("objective", "")).strip()
    if objective:
        state.objective = objective
    plan = _ensure_list(payload.get("plan"))
    if plan:
        state.plan = plan
        state.current_step = 0
    handoff_note = str(payload.get("handoff_note", "")).strip()
    if handoff_note:
        state.planner_notes = handoff_note
    risks = _ensure_list(payload.get("risks"))
    if risks:
        state.blockers = risks
    state.status = "planned"


def apply_executor_result(state: WorkflowState, payload: Dict[str, Any]) -> None:
    status = str(payload.get("status", "in_progress")).strip() or "in_progress"
    state.status = status
    completed_step = str(payload.get("completed_step", "")).strip()
    if completed_step:
        state.executor_notes = completed_step
        state.handoff_log.append(f"executor: {completed_step}")
    blockers = _ensure_list(payload.get("blockers"))
    if blockers:
        merged_blockers = list(dict.fromkeys(state.blockers + blockers))
        state.blockers = merged_blockers
    if state.plan and state.current_step < len(state.plan):
        state.current_step += 1
    next_step = str(payload.get("next_step", "")).strip()
    if next_step:
        state.handoff_log.append(f"next: {next_step}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Shared workflow state demo")
    parser.add_argument("--model", default=os.getenv("MODEL", "gpt-5"), help="OpenAI model")
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", ".workflow_state_handoff.json"), help="JSON file for shared state")
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        Console().print("[bold red]OPENAI_API_KEY is not set.[/bold red] Put it in your environment or a .env file.")
        return 2

    console = Console()
    client = OpenAI()
    state_path = Path(args.state_file).resolve()
    state = load_state(state_path)

    console.print(f"[bold]Workflow state demo[/bold] model={args.model} state_file={state_path}")
    console.print("Type /help for commands.\n")

    help_text = (
        "Commands:\n"
        "  /help    show commands\n"
        "  /state   show the shared workflow state\n"
        "  /reset   clear the workflow state file\n"
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
                console.print("[bold]Shared workflow state[/bold]")
                console.print(state.render() + "\n")
            elif cmd == "/reset":
                state = WorkflowState()
                save_state(state_path, state)
                console.print("Cleared workflow state.\n")
            elif cmd == "/exit":
                console.print("Goodbye.")
                return 0
            else:
                console.print("Unknown command. Type /help.\n")
            continue

        state.turn_count += 1
        if not state.objective.strip():
            state.objective = user_text.strip()

        planner_payload = request_json(
            client,
            args.model,
            "You are the planning agent. Produce concise, structured workflow state.",
            build_planner_prompt(state, user_text),
        )
        apply_planner_result(state, planner_payload)

        executor_payload = request_json(
            client,
            args.model,
            "You are the execution agent. Advance the shared workflow state.",
            build_executor_prompt(state),
        )
        apply_executor_result(state, executor_payload)

        save_state(state_path, state)

        console.print("[bold]Planner output[/bold]")
        console.print(Markdown(f"```json\n{json.dumps(planner_payload, indent=2)}\n```"))
        console.print("[bold]Executor output[/bold]")
        console.print(Markdown(f"```json\n{json.dumps(executor_payload, indent=2)}\n```"))
        console.print("[bold]Shared state[/bold]")
        console.print(state.render() + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
