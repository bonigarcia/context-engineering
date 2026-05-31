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

from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker


TASK_QUEUE = "context-engineering-temporal-waiting-signal"


@workflow.defn
class WaitingSignalWorkflow:
    def __init__(self) -> None:
        self.signal_message = ""

    @workflow.signal
    def resume(self, message: str) -> None:
        self.signal_message = message

    @workflow.run
    async def run(self, topic: str) -> str:
        draft = f"draft ready for {topic}"
        await workflow.wait_condition(lambda: bool(self.signal_message))
        return f"{draft}; resumed with {self.signal_message}"


async def main() -> None:
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[WaitingSignalWorkflow],
    ):
        workflow_id = "temporal-waiting-signal-demo"
        handle = await client.start_workflow(
            WaitingSignalWorkflow.run,
            "customer follow-up",
            id=workflow_id,
            task_queue=TASK_QUEUE,
        )

        print(f"Workflow started: {workflow_id}")
        await asyncio.sleep(1)
        await handle.signal(WaitingSignalWorkflow.resume, "external approval arrived")
        print(await handle.result())


if __name__ == "__main__":
    asyncio.run(main())
