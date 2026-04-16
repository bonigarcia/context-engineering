/*
 * (C) Copyright 2026 Boni Garcia (https://bonigarcia.github.io/)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */
package io.github.bonigarcia.ce;

import org.springframework.ai.mcp.annotation.McpTool;
import org.springframework.ai.mcp.annotation.McpToolParam;
import org.springframework.stereotype.Service;

import io.github.bonigarcia.ce.browser.BrowserManager;

@Service
public class BrowserService {

    private final BrowserManager browserManager = new BrowserManager();

    @McpTool(name = "open_browser", description = "Launches a new browser instance. Supports Chrome and Firefox browsers")
    public String startBrowser(
            @McpToolParam(description = "The name of the browser to open. Supported values: 'chrome', 'firefox'", required = true) String browserName) {
        return browserManager.start(browserName).message();
    }

    @McpTool(name = "navigate_url", description = "Navigate the browser to a specified URL. The browser must be started first")
    public String navigate(
            @McpToolParam(description = "The complete URL to navigate to (e.g., https://example.com)", required = true) String url) {
        return browserManager.navigate(url).message();
    }

    @McpTool(name = "close_browser", description = "Close the browser")
    public String closeBrowser() {
        return browserManager.close().message();
    }

    @McpTool(name = "get_browser_text", description = "Read the visible text of the entire page")
    public String readPageText() {
        return browserManager.readText().message();
    }

}
