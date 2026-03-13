# MCP Selenium Server with Spring-Boot

This project implements a Model Context Protocol (MCP) server using Java, [Spring-Boot](https://spring.io/projects/spring-boot), and [Selenium](https://www.selenium.dev/). The server provides tools to automate browser interactions, which can be used by AI agents to browse the web.

## Prerequisites

- [Java](https://www.oracle.com/java/technologies/downloads/) 21+
- [Maven](https://maven.apache.org/) 3.9+
- A local browser (e.g., [Chrome](https://www.google.com/chrome/), [Firefox](https://www.firefox.com/), or [Edge](https://www.microsoft.com/edge/))
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
npx @modelcontextprotocol/inspector java -jar /path/to/context-engineering-ch04-spring-boot-1.0.0.jar
```

## Output

The server communicates via standard input/output (stdio) and is intended to be used as an MCP server by an AI client.