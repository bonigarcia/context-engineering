/*
 * (C) Copyright 2025 Boni Garcia (https://bonigarcia.github.io/)
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
package io.github.bonigarcia.ce.ch04;

import java.util.List;
import java.util.Map;

import io.modelcontextprotocol.server.McpServerFeatures;
import io.modelcontextprotocol.spec.McpSchema;
import io.modelcontextprotocol.spec.McpSchema.Tool;
import reactor.core.publisher.Mono;

public class BrowserTools {

    private final BrowserService browserService;

    public BrowserTools(BrowserService browserService) {
        this.browserService = browserService;
    }

    public McpServerFeatures.AsyncToolSpecification browserStart() {
        String browserStartArgument = "open_browser";
        String browserNameArgument = "browser_name";

        McpSchema.JsonSchema inputSchema = new McpSchema.JsonSchema("object",
                Map.of(browserNameArgument, Map.of("type", "string",
                        "description",
                        "The name of the browser to open. Supported values: 'chrome', 'firefox'")),
                List.of(browserNameArgument), null, null, null);
        Tool tool = McpSchema.Tool.builder().name(browserStartArgument)
                .description(
                        "Launches a new browser instance. Supports Chrome and Firefox browsers")
                .inputSchema(inputSchema).build();

        return McpServerFeatures.AsyncToolSpecification.builder().tool(tool)
                .callHandler((exchange, args) -> {
                    String browserName = (String) args.arguments()
                            .get(browserNameArgument);
                    String result = browserService.startBrowser(browserName);
                    return Mono.just(McpSchema.CallToolResult.builder()
                            .addTextContent(result)
                            .isError(result.startsWith("Error")).build());
                }).build();
    }

    public McpServerFeatures.AsyncToolSpecification browserNavigate() {
        McpSchema.JsonSchema inputSchema = new McpSchema.JsonSchema("object",
                Map.of("url", Map.of("type", "string", "description",
                        "The complete URL to navigate to (e.g., https://example.com)")),
                List.of("url"), null, null, null);

        Tool tool = McpSchema.Tool.builder().name("navigate_url").description(
                "Navigate the browser to a specified URL. The browser must be started first")
                .inputSchema(inputSchema).build();

        return McpServerFeatures.AsyncToolSpecification.builder().tool(tool)
                .callHandler((exchange, args) -> {
                    String url = (String) args.arguments().get("url");
                    String result = browserService.navigate(url);
                    return Mono.just(McpSchema.CallToolResult.builder()
                            .addTextContent(result)
                            .isError(result.startsWith("Error")).build());
                }).build();
    }

    public McpServerFeatures.AsyncToolSpecification browserClose() {
        McpSchema.JsonSchema inputSchema = new McpSchema.JsonSchema("object",
                Map.of(), List.of(), null, null, null);

        Tool tool = McpSchema.Tool.builder().name("close_browser")
                .description("Close the browser").inputSchema(inputSchema)
                .build();

        return McpServerFeatures.AsyncToolSpecification.builder().tool(tool)
                .callHandler((exchange, args) -> {
                    String result = browserService.closeBrowser();
                    return Mono.just(McpSchema.CallToolResult.builder()
                            .addTextContent(result)
                            .isError(result.startsWith("Error")).build());
                }).build();
    }

    public McpServerFeatures.AsyncToolSpecification readPageText() {
        McpSchema.JsonSchema inputSchema = new McpSchema.JsonSchema("object",
                Map.of(), List.of(), null, null, null);

        Tool tool = McpSchema.Tool.builder().name("get_browser_text")
                .description("Read the visible text of the entire page")
                .inputSchema(inputSchema).build();

        return McpServerFeatures.AsyncToolSpecification.builder().tool(tool)
                .callHandler((exchange, args) -> {
                    String result = browserService.readPageText();
                    return Mono.just(McpSchema.CallToolResult.builder()
                            .addTextContent(result)
                            .isError(result.startsWith("Error")).build());
                }).build();
    }

}
