# MCP Selenium Server with Micronaut

This folder contains a Micronaut implementation of a basic [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server. This server provides a set of tools for an AI agent to control a web browser using [Selenium](http://selenium.dev/).  This MCP server exposes the following tools:

- `open_browser`: Launches a new browser instance (e.g., Chrome, Firefox).
- `navigate_url`: Navigates the open browser to a specified URL.
- `get_browser_text`: Retrieves the visible text content of the current page.
- `close_browser`: Closes the current browser instance.

## Prerequisites

- [Java](https://www.oracle.com/java/technologies/downloads/) 21+
- [Maven](https://maven.apache.org/) 3.9+
- A local browser (e.g., [Chrome](https://www.google.com/chrome/), [Firefox](https://www.firefox.com/))
- [Node.js](https://nodejs.org/) (only for debugging with the [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector))

## Building and running

1. Build the project:

Maven:
```bash
mvn clean package
```

Gradle:
```bash
gradle clean build
```

2. Run the server:

Maven build:
```bash
java -jar target/mcp-micronaut-1.0.0.jar
```

Gradle build:
```bash
java -jar build/libs/mcp-micronaut-all.jar
```

3. Alternatively, you can debug the MCP server using the MCP Inspector:

Maven build:
```bash
npx @modelcontextprotocol/inspector java -jar target/mcp-micronaut-1.0.0.jar
```

Gradle build:
```bash
npx @modelcontextprotocol/inspector java -jar  build/libs/mcp-micronaut-all.jar
```

## Output

The server communicates via standard input/output (stdio) and is intended to be used as an MCP server by an AI client.

If you use the MCP inspector for debugging, once connected, it will display the available tools. You can now use its user interface to execute these tools.

![MCP Inspector UI interface](/docs/img/mcp-inspector-ui.png)
