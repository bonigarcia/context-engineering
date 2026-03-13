"""
(C) Copyright 2026 Boni Garcia (https://bonigarcia.github.io/)
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import asyncio
from typing import Any, Dict
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolResult
from selenium import webdriver
from selenium.webdriver.common.by import By


class SeleniumBrowser:
    def __init__(self):
        self.driver = None

    def start_browser(self, browser_name: str) -> str:
        if self.driver:
            return "Browser is already open."
        try:
            if browser_name.lower() == "chrome":
                self.driver = webdriver.Chrome()
            elif browser_name.lower() == "firefox":
                self.driver = webdriver.Firefox()
            else:
                return f"Error: Unsupported browser: {browser_name}"
            return f"Browser '{browser_name}' started successfully."
        except Exception as e:
            return f"Error starting browser: {str(e)}"

    def navigate(self, url: str) -> str:
        if not self.driver:
            return "Error: Browser not started. Please start a browser first."
        try:
            self.driver.get(url)
            return "Navigation successful."
        except Exception as e:
            return f"Error navigating to url: {str(e)}"

    def get_text(self) -> str:
        if not self.driver:
            return "Error: Browser not started. Please start a browser first."
        try:
            return self.driver.find_element(By.TAG_NAME, "body").text
        except Exception as e:
            return f"Error reading page text: {str(e)}"

    def close_browser(self) -> str:
        if not self.driver:
            return "Error: Browser not started. Please start a browser first."
        try:
            self.driver.quit()
            self.driver = None
            return "Browser closed successfully."
        except Exception as e:
            return f"Error closing browser: {str(e)}"


browser = SeleniumBrowser()
server = Server("mcp-selenium-server")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="open_browser",
            description="Launches a new browser instance. Supports Chrome and Firefox browsers.",
            inputSchema={
                "type": "object",
                "properties": {
                    "browser_name": {
                        "type": "string",
                        "description": "The name of the browser to open. Supported values: 'chrome', 'firefox'",
                    },
                },
                "required": ["browser_name"],
            },
        ),
        Tool(
            name="navigate_url",
            description="Navigate the browser to a specified URL. The browser must be started first.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The complete URL to navigate to (e.g., https://example.com)",
                    },
                },
                "required": ["url"],
            },
        ),
        Tool(
            name="get_browser_text",
            description="Read the visible text of the entire page.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="close_browser",
            description="Close the browser.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: Dict[str, Any] | None
) -> list[TextContent]:
    """Handle tool calls."""
    if name == "open_browser":
        browser_name = arguments.get("browser_name", "chrome")
        result = browser.start_browser(browser_name)
    elif name == "navigate_url":
        url = arguments.get("url")
        result = browser.navigate(url)
    elif name == "get_browser_text":
        result = browser.get_text()
    elif name == "close_browser":
        result = browser.close_browser()
    else:
        result = f"Error: Tool '{name}' not found"

    is_error = result.startswith("Error")
    return [TextContent(type="text", text=result)]


async def main():
    """Run the server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-selenium-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
