# Secure MCP server using OAuth 2.0

This example shows how to build a secure MCP server that enforces token validation before executing sensitive operations.

## Requirements

This project requires [Python](https://www.python.org/) 3.10+, the libraries listed in `requirements.txt`.

## Steps for running this example

1. Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the server:
```bash
python secure_mcp_oauth.py
```

## Output

The server will start using the standard input and output transport. When an agent calls the get secure data tool with a valid token the server returns the requested information. If the token is invalid or missing the server provides an error message indicating that the request is unauthorized.