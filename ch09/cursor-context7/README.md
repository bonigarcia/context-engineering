# Cursor with Context7

This example uses [Upstash Context7](https://github.com/upstash/context7) as a Cursor MCP server. The coding task is a small `httpx` client helper, and it benefits from current documentation because the example depends on version-specific details such as `base_url`, timeout construction, and explicit redirect handling.

## Files

- `README.md` explains the workflow and local verification.
- `.cursor/mcp.json` shows the manual Cursor MCP configuration for Upstash Context7.
- `context7-query.md` captures the retrieval flow and the documentation facts used before coding.
- `requirements.txt` pins the library version used by the example.
- `src/http_client.py` contains the runnable helper.
- `tests/test_http_client.py` verifies the result.

## Manual Cursor Setup

1. Open this project in Cursor.
2. Add the Context7 MCP server configuration from `.cursor/mcp.json`.
3. Replace `"YOUR_CONTEXT7_API_KEY"` in the Cursor MCP configuration with your own Context7 API key, or paste your key into the equivalent Cursor MCP settings field.
4. Ask Cursor to use Context7 for the `httpx` task before generating code.

If you want a shortcut, `npx ctx7 setup --cursor` can help bootstrap the configuration, but the main artifact in this example is the explicit manual MCP setup kept in the repository.

## Local Verification

```bash
python -m venv .venv
# Activate the virtual environment in your shell.
pip install -r requirements.txt
python -m unittest discover -s tests -p "test_*.py" -v
```

The point of the example is to make current documentation retrieval explicit and inspectable inside the Cursor MCP workflow instead of reducing it to a handwritten note.
