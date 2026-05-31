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


TASK_QUEUE = "context-engineering-temporal"


@activity.defn
async def draft_response(topic: str) -> str:
    """Create a short draft that the workflow will hold until approval."""

    return f"Draft response for {topic}: keep the answer concise and context-aware."


@workflow.defn
class ApprovalWorkflow:
    def __init__(self) -> None:
        self.approved_by = ""

    @workflow.signal
    def approve(self, approver: str) -> None:
        self.approved_by = approver

    @workflow.run
    async def run(self, topic: str) -> str:
        draft = await workflow.execute_activity(
            draft_response,
            topic,
            start_to_close_timeout=timedelta(seconds=30),
        )

        await workflow.wait_condition(lambda: bool(self.approved_by))
        return f"{draft} Approved by {self.approved_by}."


async def main() -> None:
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[ApprovalWorkflow],
        activities=[draft_response],
    ):
        workflow_id = "temporal-human-approval-demo"
        handle = await client.start_workflow(
            ApprovalWorkflow.run,
            "release note for a customer escalation",
            id=workflow_id,
            task_queue=TASK_QUEUE,
        )

        print(f"Workflow started: {workflow_id}")
        print("The workflow is paused until you approve it.")
        await asyncio.to_thread(input, "Press Enter to approve and resume... ")

        await handle.signal(ApprovalWorkflow.approve, "human reviewer")
        result = await handle.result()
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
