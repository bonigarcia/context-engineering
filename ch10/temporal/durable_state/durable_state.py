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

import asyncio
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker


TASK_QUEUE = "context-engineering-temporal-durable-state"


@activity.defn
async def prepare_context(topic: str) -> str:
    """Create the durable draft state used before the pause."""

    return f"draft prepared for {topic}"


@workflow.defn
class DurableStateWorkflow:
    def __init__(self) -> None:
        self.events: list[str] = []
        self.resumed = False

    @workflow.signal
    def resume(self, note: str) -> None:
        self.events.append(f"signal:{note}")
        self.resumed = True

    @workflow.run
    async def run(self, topic: str) -> str:
        self.events.append("started")
        draft = await workflow.execute_activity(
            prepare_context,
            topic,
            start_to_close_timeout=timedelta(seconds=30),
        )
        self.events.append(draft)
        await workflow.wait_condition(lambda: self.resumed)
        self.events.append("completed")
        return " | ".join(self.events)


async def main() -> None:
    client = await Client.connect("localhost:7233")
    workflow_id = "temporal-durable-state-demo"

    async with Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[DurableStateWorkflow],
        activities=[prepare_context],
    ):
        handle = await client.start_workflow(
            DurableStateWorkflow.run,
            "chapter summary",
            id=workflow_id,
            task_queue=TASK_QUEUE,
        )

        print(f"Workflow started: {workflow_id}")
        await asyncio.sleep(1)

    print("Worker restarted; Temporal will replay the stored state.")

    async with Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[DurableStateWorkflow],
        activities=[prepare_context],
    ):
        await handle.signal(DurableStateWorkflow.resume, "worker restart complete")
        print(await handle.result())


if __name__ == "__main__":
    asyncio.run(main())
