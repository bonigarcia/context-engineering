/*
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
*/
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
    'get_browser_text',
    {
        description: 'Read the visible text of the entire page',
        inputSchema: z.object({}),
    },
    async () => {
        if (!driver) {
            return { error: 'Browser is not open.' };
        }
        try {
            const body = await driver.findElement(By.css('body'));
            const text = await body.getText();
            return { content: [{ type: 'text', text }] };
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