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


def build_trace_db(root: Path) -> JsonDb:
    return JsonDb(db_path=str(root / "audit_traces.json"))


def build_agent(root: Path, trace_db: JsonDb | None = None) -> Agent:
    return Agent(
        name="Audit Traces",
        model=OpenAIResponses(id="gpt-5-mini"),
        db=trace_db or build_trace_db(root),
        store_events=True,
        markdown=True,
        instructions=(
            "Keep the run small and explain what context was used. The traces should make the "
            "input, tool usage, and response auditable after the run."
        ),
    )


def main() -> None:
    root = Path(__file__).resolve().parent
    db = build_trace_db(root)
    agent = build_agent(root, db)
    agent.print_response("Summarize the context used for this run.", stream=True)
    stats, count = db.get_trace_stats(agent_id=agent.id, limit=5)
    print(f"\nTrace stats: {count} record(s)")
    print(stats)


if __name__ == "__main__":
    main()
