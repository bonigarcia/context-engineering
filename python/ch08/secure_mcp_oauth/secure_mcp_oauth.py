from mcp.server.fastmcp import FastMCP
import sys

# This example demonstrates a secure MCP server that requires OAuth 2.0 validation
# The server simulates the verification of a bearer token before executing tool logic

# Initialize the MCP server
mcp = FastMCP("Secure Database Server")

def verify_oauth_token(token: str) -> bool:
    # This is a simulation of a token validation process
    # In a real scenario, this function would verify the token against an identity provider
    # It might check the signature, expiration, and required scopes
    valid_tokens = ["valid_oauth_token_123"]
    return token in valid_tokens

@mcp.tool()
def get_secure_data(token: str, query: str) -> str:
    """
    Retrieves data from a secure repository after validating the OAuth token.
    """
    if not verify_oauth_token(token):
        return "Error: Unauthorized. A valid OAuth 2.0 token is required."
    
    # Logic to fetch data from the repository
    return f"Secure data for query '{query}': [Sample Result]"

if __name__ == "__main__":
    # The server starts and waits for requests via stdio
    mcp.run()
