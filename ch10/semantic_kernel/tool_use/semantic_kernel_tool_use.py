"""Runnable Semantic Kernel tool-use example."""

from __future__ import annotations

import asyncio


def lookup_example_code() -> str:
    """Return the fixed code word used by the example."""

    return "SK-TOOL-42"


class ToolUsePlugin:
    """Semantic Kernel plugin wrapper for the fixed example tool."""

    def lookup_example_code(self) -> str:
        return lookup_example_code()


async def _run_tool_use_example() -> str:
    try:
        from semantic_kernel import Kernel
    except ImportError:  # pragma: no cover - exercised only in runtime setups
        from semantic_kernel.kernel import Kernel

    try:
        from semantic_kernel.functions import kernel_function
    except ImportError:  # pragma: no cover - exercised only in runtime setups
        from semantic_kernel.functions.kernel_function import kernel_function

    class AnnotatedToolUsePlugin(ToolUsePlugin):
        @kernel_function(name="lookup_example_code")
        def lookup_example_code(self) -> str:
            return super().lookup_example_code()

    kernel = Kernel()
    kernel.add_plugin(AnnotatedToolUsePlugin(), plugin_name="tool_use")

    result = await kernel.invoke(
        plugin_name="tool_use",
        function_name="lookup_example_code",
    )
    return getattr(result, "value", result)


def main() -> None:
    output = asyncio.run(_run_tool_use_example())
    print(f"Tool-backed example output: {output}")


if __name__ == "__main__":
    main()
