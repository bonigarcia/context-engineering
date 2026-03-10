# Using MCP Tools with LlamaIndex

This example demonstrates how to integrate Model Context Protocol (MCP) servers as tools within LlamaIndex agents. MCP provides a standardized way for agents to interact with external services and data sources. By converting an MCP server definition into a LlamaIndex tool, agents can leverage the capabilities of these services to enrich their context and perform complex tasks.

This example sets up a very basic dummy HTTP server that simulates an MCP server (for simplicity, it doesn't fully implement the MCP specification but provides a callable endpoint). It then uses `BasicMCPClient` to convert this simulated MCP server into a LlamaIndex tool. Finally, an `OpenAIAgent` is configured with this tool, allowing it to interact with the MCP service and use its functionality to answer queries.

## Requirements

* Python 3.8+
* An OpenAI API key set as an environment variable (`OPENAI_API_KEY`).

## Steps for running this example

1.  Install dependencies:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    ```

2. Set environment variables:
    Ensure your OpenAI API key is set as an environment variable. You can do this by creating a `.env` file in the example directory with the following content:
    ```
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    ```
    Replace `"YOUR_OPENAI_API_KEY"` with your actual OpenAI API key.

3. Run the script:
    ```bash
    python mcp_tool_use.py
    ```
    The script will start a dummy MCP server and then demonstrate an agent interacting with it.

## Output

The script will first confirm that the dummy MCP server has started. Then, it will show an interaction with the agent where it calls the MCP tool to get a response. You should see output indicating the tool call and its result.
