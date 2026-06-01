from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent))

from semantic_kernel_planner_executor import build_plan, execute_plan


def test_build_plan_returns_three_step_plan_for_supported_request():
    assert build_plan(
        "Organize a three-step plan for a small day-of-week reminder workflow."
    ) == [
        "Capture the reminder request",
        "Create three reminder actions",
        "Execute the reminder actions in order",
    ]


def test_execute_plan_returns_deterministic_step_results():
    assert execute_plan([
        "Capture the reminder request",
        "Create three reminder actions",
        "Execute the reminder actions in order",
    ]) == [
        "done: Capture the reminder request",
        "done: Create three reminder actions",
        "done: Execute the reminder actions in order",
    ]
