# Context7 Query

Cursor is connected to Upstash Context7 through MCP before it generates the `httpx` helper.

- Library: `httpx`
- Version: `0.27.2`

## Retrieval Trace

1. Resolve the `httpx` library through Context7 MCP.
2. Query the version-aware docs for client construction and timeout options.
3. Apply the retrieved guidance to the small helper in `src/http_client.py`.

## Retrieved Guidance

- `httpx.Client` accepts `base_url`.
- `httpx.Timeout` can use a default timeout plus `connect`.
- `follow_redirects=True` is explicit.

MCP-based retrieval matters here because Cursor can ground the generated helper in current library documentation instead of stale remembered API details.
