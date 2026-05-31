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
    researcher = Agent(
        role="Researcher",
        goal="Gather concise facts about {topic}",
        backstory="You are a careful researcher who collects only the most relevant context.",
        verbose=True,
    )

    writer = Agent(
        role="Writer",
        goal="Write a short summary about {topic} using the research provided",
        backstory="You turn research notes into a clear, readable summary.",
        verbose=True,
    )

    research_task = Task(
        description="Research {topic} and list the key points needed for a short summary.",
        expected_output="A brief research note with the key points about the topic.",
        agent=researcher,
    )

    writing_task = Task(
        description="Write a short summary about {topic} using the research notes.",
        expected_output="A concise summary in Markdown.",
        agent=writer,
        context=[research_task],
    )

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(inputs={"topic": "context engineering"})
    print(result)


if __name__ == "__main__":
    main()
