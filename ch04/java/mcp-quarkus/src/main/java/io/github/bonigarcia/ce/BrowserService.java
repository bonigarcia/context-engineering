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

import io.github.bonigarcia.ce.browser.BrowserManager;
import io.quarkiverse.mcp.server.Tool;
import io.quarkiverse.mcp.server.ToolArg;
import jakarta.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class BrowserService {

    private final BrowserManager browserManager = new BrowserManager();

    @Tool(description = "Launches a new browser instance. Supports Chrome and Firefox browsers")
    public String open_browser(
            @ToolArg(description = "The name of the browser to open. Supported values: 'chrome', 'firefox'") String browser_name) {
        return browserManager.start(browser_name).message();
    }

    @Tool(description = "Navigate the browser to a specified URL. The browser must be started first")
    public String navigate_url(
            @ToolArg(description = "The complete URL to navigate to (e.g., https://example.com)") String url) {
        return browserManager.navigate(url).message();
    }

    @Tool(description = "Close the browser")
    public String close_browser() {
        return browserManager.close().message();
    }

    @Tool(description = "Read the visible text of the entire page")
    public String get_browser_text() {
        return browserManager.readText().message();
    }

}
