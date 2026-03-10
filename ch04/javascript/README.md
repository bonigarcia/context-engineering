# MCP Selenium Server in JavaScript

This folder contains a JavaScript implementation of a basic [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server. This server provides a set of tools for an AI agent to control a web browser using [Selenium](http://selenium.dev/).

## Features

The `mcp-selenium-server.js` exposes the following tools:

- `open_browser`: Launches a new browser instance (e.g., Chrome, Firefox).
- `navigate_url`: Navigates the open browser to a specified URL.
- `read_browser_text`: Retrieves the visible text content of the current page.
- `close_browser`: Closes the current browser instance.

## Prerequisites

- [Node.js](https://nodejs.org/) installed.
- A local browser (like Google Chrome or Mozilla Firefox) installed.

## Installation

1. Open a terminal in this `javascript` folder.
2. Run the following command to install the required dependencies:

```bash
npm install
```

## Usage

To start the server, run the following command in this `javascript` folder:

```bash
npm start
```

The server will start and listen for MCP requests on standard input.

## Debugging with mcp-inspector

The `mcp-inspector` is a powerful tool for debugging MCP servers. You can use it to interact with this `mcp-selenium-server` and test its functionality.

1.  Get the JavaScript sources and go to the proper directory:
    ```bash
    git clone https://github.com/bonigarcia/context-engineering
    cd context-engineering/javascript/ch04
    ```

2.  Start the `mcp-selenium-server` with `mcp-inspector`:
    ```bash
    npx @modelcontextprotocol/inspector node mcp-selenium-server.js
    ```
    This will open a web UI at http://localhost:6274/

3.  Connect with `mcp-selenium-server`:
    Click on button "Connect" to start `mcp-selenium-server`.

4.  Interact with the server:
    Once connected, `mcp-inspector` will display the available tools. You can now send commands to the `mcp-selenium-server`. Example workflow in `mcp-inspector`:

    - Open a browser:
      ```
      call open_browser {"browser_name": "chrome"}
      ```
      (or "firefox")

    - Navigate to a URL:
      ```
      call navigate_url {"url": "https://modelcontextprotocol.io/"}
      ```

    - Read page text:
      ```
      call read_browser_text {}
      ```

    - Close the browser:
      ```
      call close_browser {}
      ```

    `mcp-inspector` will display the responses from the `mcp-selenium-server`, allowing you to see the results of each tool call and debug any issues.

    ![MCP Inspector UI interface](/docs/img/mcp-inspector-ui.png)