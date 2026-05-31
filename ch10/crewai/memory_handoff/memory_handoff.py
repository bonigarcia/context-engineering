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
    recorder = Agent(
        role="Recorder",
        goal="Capture durable notes about {topic}",
        backstory="You write down the important facts for later reuse.",
        verbose=True,
    )

    responder = Agent(
        role="Responder",
        goal="Answer {topic} using the remembered notes",
        backstory="You reuse earlier context instead of starting over.",
        verbose=True,
    )

    note_task = Task(
        description="Write three durable notes about {topic}.",
        expected_output="Three short bullet points.",
        agent=recorder,
    )

    response_task = Task(
        description="Answer {topic} using the notes that were just remembered.",
        expected_output="A short answer in Markdown.",
        agent=responder,
        context=[note_task],
    )

    crew = Crew(
        agents=[recorder, responder],
        tasks=[note_task, response_task],
        process=Process.sequential,
        memory=True,
        verbose=True,
    )

    result = crew.kickoff(inputs={"topic": "memory handoff"})
    print(result)


if __name__ == "__main__":
    main()
