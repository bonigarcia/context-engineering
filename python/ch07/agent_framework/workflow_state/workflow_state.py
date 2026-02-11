import asyncio
import tempfile
import uuid
from pathlib import Path
from typing import Optional

from typing_extensions import Never

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler


class FileReadExecutor(Executor):
    """Reads a file and stores content in workflow state, then passes the state key downstream."""

    @handler
    async def handle(self, file_path: str, ctx: WorkflowContext[str]) -> None:
        content = Path(file_path).read_text(encoding="utf-8")

        file_id = str(uuid.uuid4())
        ctx.set_state(file_id, content)

        # Pass only the key downstream
        await ctx.send_message(file_id)


class WordCountingExecutor(Executor):
    """Retrieves content from workflow state and yields a word-count output."""

    @handler
    async def handle(self, file_id: str, ctx: WorkflowContext[Never, int]) -> None:
        file_content: Optional[str] = ctx.get_state(file_id)
        if file_content is None:
            raise ValueError("File content not found in workflow state")

        word_count = len(file_content.split())
        await ctx.yield_output(word_count)


async def main() -> None:
    # Create a temporary file so the example is self-contained
    tmp_dir = Path(tempfile.mkdtemp(prefix="maf_state_demo_"))
    file_path = tmp_dir / "sample.txt"
    file_path.write_text(
        "Hello world.\n"
        "This is a workflow state demo.\n"
        "Executors share data through workflow state.\n",
        encoding="utf-8",
    )

    print(f"Temp file: {file_path}")

    # Create executor instances
    file_reader = FileReadExecutor(id="file-read")
    word_counter = WordCountingExecutor(id="word-count")
    workflow = (
        WorkflowBuilder(name="state-demo", start_executor=file_reader)
        .add_edge(file_reader, word_counter)
        .build()
    )

    events = await workflow.run(str(file_path))

    # Output collection can vary by build; handle both common patterns.
    if hasattr(events, "get_outputs"):
        outputs = events.get_outputs()
        if outputs:
            print(f"Word count: {outputs[0]}")
            return

    # Fallback: some builds expose outputs directly
    outputs = getattr(events, "outputs", None)
    if outputs:
        print(f"Word count: {outputs[0]}")
    else:
        print("No outputs produced.")


if __name__ == "__main__":
    asyncio.run(main())
