# MCP Selenium Server with Spring-Boot

This folder contains a Spring-Boot implementation of a basic [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server. This server provides a set of tools for an AI agent to control a web browser using [Selenium](http://selenium.dev/).  This MCP server exposes the following tools:

- `open_browser`: Launches a new browser instance (e.g., Chrome, Firefox).
- `navigate_url`: Navigates the open browser to a specified URL.
- `read_browser_text`: Retrieves the visible text content of the current page.
- `close_browser`: Closes the current browser instance.

## Prerequisites

- [Java](https://www.oracle.com/java/technologies/downloads/) 21+
- [Maven](https://maven.apache.org/) 3.9+
- A local browser (e.g., [Chrome](https://www.google.com/chrome/), [Firefox](https://www.firefox.com/))
- [Node.js](https://nodejs.org/) (only for debugging with the [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector))

## Building and running

1. Build the project:
```bash
mvn clean package
```

2. Run the server:
```bash
java -jar target/context-engineering-ch04-spring-boot-1.0.0.jar
```

3. Alternatively, you can debug the MCP server using the MCP Inspector:
```bash
npx @modelcontextprotocol/inspector java -jar target/context-engineering-ch04-spring-boot-1.0.0.jar
```

## Output

The server communicates via standard input/output (stdio) and is intended to be used as an MCP server by an AI client.