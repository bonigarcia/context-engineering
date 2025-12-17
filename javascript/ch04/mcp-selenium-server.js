import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from 'zod';
import { Builder, By } from 'selenium-webdriver';

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
  'navigate_url',
  {
    description: 'Navigate the browser to a specified URL. The browser must be started first',
    inputSchema: z.object({
      url: z.string().describe('The complete URL to navigate to (e.g., https://example.com)'),
    }),
  },
  async ({ url }) => {
    if (!driver) {
      return { error: 'Browser is not open.' };
    }
    try {
      await driver.get(url);
      return { success: `Navigated to ${url}` };
    } catch (error) {
      return { error: `Failed to navigate to ${url}: ${error.message}` };
    }
  },
);

server.registerTool(
  'read_browser_text',
  {
    description: 'Get the visible text of the entire page',
    inputSchema: z.object({}),
  },
  async () => {
    if (!driver) {
      return { error: 'Browser is not open.' };
    }
    try {
      const body = await driver.findElement(By.css('body'));
      const text = await body.getText();
      return { text };
    } catch (error) {
      return { error: `Failed to read browser text: ${error.message}` };
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