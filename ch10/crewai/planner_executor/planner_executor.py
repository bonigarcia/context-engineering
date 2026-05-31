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
    planner = Agent(
        role="Planner",
        goal="Create a short execution plan for {goal}",
        backstory="You turn a request into a small, ordered plan.",
        verbose=True,
    )

    executor = Agent(
        role="Executor",
        goal="Carry out the plan for {goal} and report the result",
        backstory="You follow the plan and turn it into a concise outcome.",
        verbose=True,
    )

    plan_task = Task(
        description="Create a 3-step plan for {goal}.",
        expected_output="A numbered 3-step plan.",
        agent=planner,
    )

    execute_task = Task(
        description="Execute the plan for {goal} using the planner's notes.",
        expected_output="A short execution summary in Markdown.",
        agent=executor,
        context=[plan_task],
    )

    crew = Crew(
        agents=[planner, executor],
        tasks=[plan_task, execute_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(inputs={"goal": "a small context-engineering demo"})
    print(result)


if __name__ == "__main__":
    main()
