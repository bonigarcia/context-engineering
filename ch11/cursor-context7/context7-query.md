# Context7 Query

Cursor is connected to Upstash Context7 through MCP before it generates the FastAPI backlog scoring endpoint.

- Library: `fastapi`
- Version: `0.111.0`

## Retrieval Trace

1. Resolve the `fastapi` library through Context7 MCP.
2. Query the version-aware docs for routing decorators, request validation using Pydantic, and response models.
3. Apply the retrieved guidance to the backlog scoring endpoint in `src/backlog.py`.

## Retrieved Guidance

- `fastapi.FastAPI` provides routing decorators like `@app.post()`.
- Pydantic's `BaseModel` and `Field` are used for request validation, allowing constraints like `ge=0` and `le=5` to enforce values within range.
- `response_model` parameter in path decorators enables response validation and serialization using a return schema.

MCP-based retrieval matters here because Cursor can ground the generated helper in current library documentation instead of stale remembered API details.
