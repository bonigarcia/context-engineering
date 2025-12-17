import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from 'zod';
import { Builder } from 'selenium-webdriver';

let driver;

const server = new McpServer({
  name: 'mcp-selenium-server',
  version: '1.0.0',
});

server.registerTool(
  'open_browser',
  {
    description: 'Launches a new browser instance.',
    inputSchema: z.object({
      browser_name: z.string().describe('The name of the browser to open (e.g., "chrome", "firefox").'),
    }),
  },
  async ({ browser_name }) => {
    if (driver) {
      return { error: 'Browser is already open.' };
    }
    try {
      driver = await new Builder().forBrowser(browser_name).build();
      return { success: `Browser "${browser_name}" started successfully.` };
    } catch (error) {
      return { error: `Failed to open browser: ${error.message}` };
    }
  },
);

server.registerTool(
  'close_browser',
  {
    description: 'Closes the browser.',
    inputSchema: z.object({}),
  },
  async () => {
    if (!driver) {
      return { error: 'Browser is not open.' };
    }
    try {
      await driver.quit();
      driver = null;
      return { success: 'Browser closed.' };
    } catch (error) {
      return { error: `Failed to close browser: ${error.message}` };
    }
  },
);

// Start MCP server
const transport = new StdioServerTransport();
await server.connect(transport);