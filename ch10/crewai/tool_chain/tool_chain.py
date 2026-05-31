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

from crewai import Agent, Crew, Process, Task
from crewai.tools import tool


@tool("topic_fact_pack")
def topic_fact_pack(topic: str) -> str:
    """Return a short fact pack for a topic."""
    return (
        f"Fact pack for {topic}:\n"
        f"- Keep the scope small.\n"
        f"- Gather only the facts needed for a short draft.\n"
        f"- Turn the facts into a concise explanation."
    )


@tool("topic_risk_check")
def topic_risk_check(topic: str) -> str:
    """Return one simple risk note for a topic."""
    return f"Risk check for {topic}: avoid over-explaining and keep the answer focused."


def main() -> None:
    gatherer = Agent(
        role="Gatherer",
        goal="Use tools to collect useful context about {topic}",
        backstory="You assemble a tiny fact pack before anyone writes.",
        tools=[topic_fact_pack, topic_risk_check],
        verbose=True,
    )

    writer = Agent(
        role="Writer",
        goal="Write a short answer about {topic} from the gathered context",
        backstory="You turn gathered context into a clean final response.",
        verbose=True,
    )

    gather_task = Task(
        description="Use the tools to gather a small fact pack and one risk note for {topic}.",
        expected_output="A short fact pack and a risk note.",
        agent=gatherer,
    )

    write_task = Task(
        description="Write the final answer about {topic} using the gathered context.",
        expected_output="A concise answer in Markdown.",
        agent=writer,
        context=[gather_task],
    )

    crew = Crew(
        agents=[gatherer, writer],
        tasks=[gather_task, write_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(inputs={"topic": "tool chains"})
    print(result)


if __name__ == "__main__":
    main()
