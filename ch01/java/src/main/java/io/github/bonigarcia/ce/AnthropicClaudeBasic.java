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

import java.util.stream.Collectors;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

public class AnthropicClaudeBasic implements AutoCloseable {

    AnthropicClient client;
    Model model;
    double temperature;
    long thinkingBudget;

    public AnthropicClaudeBasic(Model model, double temperature,
            long thinkingBudget) {
        this.model = model;
        this.temperature = temperature;
        this.thinkingBudget = thinkingBudget;

        // ANTHROPIC_API_KEY should be set as an environment variable
        client = AnthropicOkHttpClient.fromEnv();
    }

    public String queryModel(String prompt) {
        MessageCreateParams.Builder builder = MessageCreateParams.builder()
                .maxTokens(2048).addUserMessage(prompt).model(model);
        if (thinkingBudget > 0) {
            builder.enabledThinking(thinkingBudget).temperature(1);
        } else {
            builder.temperature(temperature);
        }

        Message response = client.messages().create(builder.build());
        return response.content().stream()
                .flatMap(contentBlock -> contentBlock.text().stream())
                .map(textBlock -> textBlock.text())
                .collect(Collectors.joining());
    }

    @Override
    public void close() {
        client.close();
    }

    public static void main(String[] args) {
        Model model = Model.CLAUDE_SONNET_4_20250514;
        double temperature = 0;
        long thinkingBudget = 1024;
        try (AnthropicClaudeBasic claude = new AnthropicClaudeBasic(model,
                temperature, thinkingBudget)) {
            String prompt = "How many tokens is your context window?";
            String response = claude.queryModel(prompt);

            System.out.println("User query: " + prompt);
            System.out.println("Response: " + response);
        }
    }

}