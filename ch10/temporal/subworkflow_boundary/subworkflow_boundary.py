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


TASK_QUEUE = "context-engineering-temporal-subworkflow-boundary"


@workflow.defn
class ChildWorkflow:
    @workflow.run
    async def run(self, topic: str) -> str:
        return f"child summary for {topic}"


@workflow.defn
class ParentWorkflow:
    @workflow.run
    async def run(self, topic: str) -> str:
        child_summary = await workflow.execute_child_workflow(
            ChildWorkflow.run,
            topic,
            id=f"{workflow.info().workflow_id}/child",
        )
        return f"parent boundary kept tight: {child_summary}"


async def main() -> None:
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[ParentWorkflow, ChildWorkflow],
    ):
        workflow_id = "temporal-subworkflow-boundary-demo"
        handle = await client.start_workflow(
            ParentWorkflow.run,
            "customer support summary",
            id=workflow_id,
            task_queue=TASK_QUEUE,
        )

        print(f"Workflow started: {workflow_id}")
        print(await handle.result())


if __name__ == "__main__":
    asyncio.run(main())
