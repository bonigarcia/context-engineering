"""Runnable Semantic Kernel planner/executor process example."""

from __future__ import annotations

import asyncio

from pydantic import BaseModel, Field

REQUEST = "Organize a three-step plan for a small day-of-week reminder workflow."
PLAN_STEPS = [
    "Capture the reminder request",
    "Create three reminder actions",
    "Execute the reminder actions in order",
]


def build_plan(request: str) -> list[str]:
    """Return the fixed three-step plan for the supported request."""

    if request != REQUEST:
        raise ValueError("Unexpected request for the planner example")
    return PLAN_STEPS.copy()


def execute_plan(plan: list[str]) -> list[str]:
    """Return deterministic execution output for each plan step."""

    return [f"done: {step}" for step in plan]


class PlannerState(BaseModel):
    request: str | None = None
    plan: list[str] = Field(default_factory=list)


class ExecutorState(BaseModel):
    plan: list[str] = Field(default_factory=list)
    execution: list[str] = Field(default_factory=list)


try:
    from semantic_kernel import Kernel
except ImportError:  # pragma: no cover - exercised only in runtime setups
    from semantic_kernel.kernel import Kernel

try:
    from semantic_kernel.functions import kernel_function
except ImportError:  # pragma: no cover - exercised only in runtime setups
    from semantic_kernel.functions.kernel_function import kernel_function

from semantic_kernel.processes import ProcessBuilder
from semantic_kernel.processes.kernel_process import KernelProcessEvent, KernelProcessStep, KernelProcessStepState
from semantic_kernel.processes.local_runtime.local_kernel_process import start


class PlannerStep(KernelProcessStep):
    async def activate(self, state: KernelProcessStepState) -> None:
        resolved_state = state.state or PlannerState()
        state.state = resolved_state
        self.state = resolved_state

    @kernel_function(name="plan")
    def plan(self, request: str) -> list[str]:
        plan = build_plan(request)
        self.state.request = request
        self.state.plan = plan
        return plan


class ExecutorStep(KernelProcessStep):
    async def activate(self, state: KernelProcessStepState) -> None:
        resolved_state = state.state or ExecutorState()
        state.state = resolved_state
        self.state = resolved_state

    @kernel_function(name="execute")
    def execute(self, plan: list[str]) -> list[str]:
        execution = execute_plan(plan)
        self.state.plan = plan
        self.state.execution = execution
        return execution


def _build_process() -> ProcessBuilder:
    process = ProcessBuilder(name="day_of_week_reminder_process")
    planner = process.add_step(PlannerStep, name="planner")
    executor = process.add_step(ExecutorStep, name="executor")

    process.on_input_event("start").send_event_to(planner)
    planner.on_function_result("plan").send_event_to(executor)
    return process


async def _run_process() -> tuple[list[str], list[str]]:
    kernel = Kernel()
    process = _build_process().build()
    context = await start(process, kernel, KernelProcessEvent(id="start", data=REQUEST))
    process_state = await context.get_state()

    planner_state = process_state.steps[0].state.state
    executor_state = process_state.steps[1].state.state

    if not isinstance(planner_state, PlannerState) or not isinstance(executor_state, ExecutorState):
        raise RuntimeError("The planner/executor process did not produce the expected state.")

    return planner_state.plan, executor_state.execution


def main() -> None:
    plan, output = asyncio.run(_run_process())

    print("Plan:")
    for index, step in enumerate(plan, start=1):
        print(f"{index}. {step}")

    print("Execution:")
    for line in output:
        print(line)


if __name__ == "__main__":
    main()
