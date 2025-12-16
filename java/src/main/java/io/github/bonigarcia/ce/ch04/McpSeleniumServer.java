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

import java.util.concurrent.CountDownLatch;

import io.modelcontextprotocol.json.McpJsonMapper;
import io.modelcontextprotocol.server.McpAsyncServer;
import io.modelcontextprotocol.server.McpServer;
import io.modelcontextprotocol.server.transport.StdioServerTransportProvider;
import io.modelcontextprotocol.spec.McpSchema;

public class McpSeleniumServer {

    public static void main(String[] args) throws Exception {
        BrowserTools tools = new BrowserTools(new BrowserService());
        var transportProvider = new StdioServerTransportProvider(
                McpJsonMapper.createDefault());

        McpAsyncServer server = McpServer.async(transportProvider)
                .serverInfo("mcp-selenium-server", "1.0.0")
                .capabilities(McpSchema.ServerCapabilities.builder().tools(true)
                        .logging().build())
                .tools(tools.browserStart(), tools.browserNavigate(),
                        tools.browserClose())
                .build();

        CountDownLatch keepAlive = new CountDownLatch(1);

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            try {
                server.close();
            } finally {
                keepAlive.countDown();
            }
        }));

        // Block forever until the Java process is terminated
        keepAlive.await();
    }
}
