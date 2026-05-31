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
from temporalio.common import RetryPolicy
from temporalio.worker import Worker


TASK_QUEUE = "context-engineering-temporal-retry-resume"


@activity.defn
async def flaky_context_step(topic: str) -> str:
    """Fail once to show Temporal retrying a durable step."""

    if activity.info().attempt == 1:
        raise RuntimeError("transient context fetch failed")

    return f"refined context for {topic}"


@workflow.defn
class RetryResumeWorkflow:
    def __init__(self) -> None:
        self.status = "starting"

    @workflow.run
    async def run(self, topic: str) -> str:
        self.status = "waiting for retry"
        detail = await workflow.execute_activity(
            flaky_context_step,
            topic,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=1),
                backoff_coefficient=2.0,
                maximum_attempts=3,
            ),
        )

        self.status = "done"
        return f"{self.status}: {detail}"


async def main() -> None:
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[RetryResumeWorkflow],
        activities=[flaky_context_step],
    ):
        workflow_id = "temporal-retry-resume-demo"
        handle = await client.start_workflow(
            RetryResumeWorkflow.run,
            "AI draft recovery",
            id=workflow_id,
            task_queue=TASK_QUEUE,
        )

        print(f"Workflow started: {workflow_id}")
        print("The activity fails once, then Temporal retries it.")
        print(await handle.result())


if __name__ == "__main__":
    asyncio.run(main())
