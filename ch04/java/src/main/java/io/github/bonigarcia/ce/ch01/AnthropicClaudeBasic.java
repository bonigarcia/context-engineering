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
package io.github.bonigarcia.ce.ch01;

import java.util.concurrent.CompletableFuture;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

public class AnthropicClaudeBasic {

    public static void main(String[] args) {
        // Ensure ANTHROPIC_API_KEY is set in your environment
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        String prompt = "How many tokens is your context window?";

        MessageCreateParams params = MessageCreateParams.builder()
                .maxTokens(1024L).addUserMessage(prompt)
                .model(Model.CLAUDE_SONNET_4_20250514).build();
        CompletableFuture<Message> future = client.async().messages()
                .create(params);

        future.thenAccept(response -> {
            String output = response.content().get(0).asText().text();
            System.out.println("User query: " + prompt);
            System.out.println("Response: " + output);
        }).join();

        client.close();
    }

}