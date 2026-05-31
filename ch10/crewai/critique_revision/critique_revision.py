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


def main() -> None:
    writer = Agent(
        role="Writer",
        goal="Draft a short answer about {topic}",
        backstory="You write a clear first pass quickly.",
        verbose=True,
    )

    critic = Agent(
        role="Critic",
        goal="Find the weakest part of the draft about {topic}",
        backstory="You give blunt but useful feedback.",
        verbose=True,
    )

    reviser = Agent(
        role="Reviser",
        goal="Improve the answer about {topic} using the critique",
        backstory="You turn feedback into a better final draft.",
        verbose=True,
    )

    draft_task = Task(
        description="Write a 2-paragraph draft about {topic}.",
        expected_output="A short draft in Markdown.",
        agent=writer,
    )

    critique_task = Task(
        description="Critique the draft about {topic} and name one concrete improvement.",
        expected_output="A concise critique with one actionable fix.",
        agent=critic,
        context=[draft_task],
    )

    revise_task = Task(
        description="Revise the original draft about {topic} using the critique.",
        expected_output="An improved final answer in Markdown.",
        agent=reviser,
        context=[draft_task, critique_task],
    )

    crew = Crew(
        agents=[writer, critic, reviser],
        tasks=[draft_task, critique_task, revise_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(inputs={"topic": "context handoff"})
    print(result)


if __name__ == "__main__":
    main()
