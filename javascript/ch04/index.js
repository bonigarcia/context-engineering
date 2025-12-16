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
    description: 'Opens a browser window using Selenium.',
    inputSchema: z.object({
      browser: z.string().describe('The name of the browser to open (e.g., "chrome", "firefox").'),
    }),
  },
  async ({ browser }) => {
    if (driver) {
      return { error: 'Browser is already open.' };
    }
    try {
      driver = await new Builder().forBrowser(browser).build();
      return { success: `Browser "${browser}" opened.` };
    } catch (error) {
      return { error: `Failed to open browser: ${error.message}` };
    }
  },
);

server.registerTool(
  'close_browser',
  {
    description: 'Closes the browser window.',
    inputSchema: z.object({}), // No parameters for close_browser
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

// Start the server
const transport = new StdioServerTransport();
await server.connect(transport);