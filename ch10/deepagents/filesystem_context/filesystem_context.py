from __future__ import annotations

try:
    from deepagents import create_deep_agent
except ImportError:  # pragma: no cover - lets tests monkeypatch the builder
    create_deep_agent = None

try:
    from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
    from deepagents.backends.utils import create_file_data
    from langgraph.store.memory import InMemoryStore
except ImportError:  # pragma: no cover - keep the example importable without optional deps
    CompositeBackend = None
    StateBackend = None
    StoreBackend = None
    create_file_data = None
    InMemoryStore = None


MODEL = "openai:gpt-5.4"
MEMORY_PATH = "/memories/AGENTS.md"
WORKSPACE_PATH = "/workspace/notes.md"
NAMESPACE = ("deepagents",)
DEPENDENCY_ERROR = (
    "filesystem_context requires deepagents and langgraph backends; "
    "install ch10/deepagents/requirements.txt"
)


def _namespace(_: str) -> tuple[str, ...]:
    return NAMESPACE


def build_store() -> InMemoryStore:
    if InMemoryStore is None or create_file_data is None:
        raise RuntimeError(DEPENDENCY_ERROR)

    store = InMemoryStore()
    store.put(NAMESPACE, MEMORY_PATH, create_file_data("# Memory\n- Keep shared notes short\n"))
    store.put(NAMESPACE, WORKSPACE_PATH, create_file_data("# Workspace\n- Seeded by the filesystem example\n"))
    return store


def build_backend() -> CompositeBackend:
    if CompositeBackend is None or StateBackend is None or StoreBackend is None:
        raise RuntimeError(DEPENDENCY_ERROR)

    return CompositeBackend(
        default=StateBackend(),
        routes={
            "/memories/": StoreBackend(namespace=_namespace),
            "/workspace/": StoreBackend(namespace=_namespace),
        },
    )


def build_agent():
    if create_deep_agent is None:
        raise RuntimeError(DEPENDENCY_ERROR)

    store = build_store()
    backend = build_backend()

    return create_deep_agent(
        model=MODEL,
        memory=[MEMORY_PATH],
        backend=backend,
        store=store,
        tools=[],
        system_prompt=(
            "You manage filesystem-backed context explicitly. Read and update memory and "
            "workspace files through the routed paths instead of keeping hidden state."
        ),
    )


def main() -> None:
    agent = build_agent()
    result = agent.invoke(
        {
            "messages": [
                (
                    "user",
                    "Use the memory and workspace files to summarize what the example seeds.",
                )
            ]
        }
    )
    print(result)


if __name__ == "__main__":
    main()
