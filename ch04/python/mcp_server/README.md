# MCP Selenium server with Python

This folder contains a Python implementation of a basic [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server. This server provides a set of tools for an AI agent to control a web browser using [Selenium](http://selenium.dev/).  This MCP server exposes the following tools:

- `open_browser`: Launches a new browser instance (e.g., Chrome, Firefox).
- `navigate_url`: Navigates the open browser to a specified URL.
- `read_browser_text`: Retrieves the visible text content of the current page.
- `close_browser`: Closes the current browser instance.

## Prerequisites

- [Python](https://www.python.org/) 3.6+
- A local browser (e.g., [Chrome](https://www.google.com/chrome/), [Firefox](https://www.firefox.com/))
- [Node.js](https://nodejs.org/) (only for debugging with the [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector))

## Building and running

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the server:
```bash
python mcp_selenium_server.py
```

3. Alternatively, you can debug the MCP server using the MCP Inspector:
```bash
npx @modelcontextprotocol/inspector python mcp_selenium_server.py
```

## Output

The server communicates via standard input/output (stdio) and is intended to be used as an MCP server by an AI client.

If you use the MCP inspector for debugging, once connected, it will display the available tools. You can now use its user interface to execute these tools.

![MCP Inspector UI interface](/docs/img/mcp-inspector-ui.png)