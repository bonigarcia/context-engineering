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

import java.util.Optional;
import java.util.stream.Collectors;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;

public class AnthropicClaudeSystemPrompt {

    String queryModel(Optional<String> instructions, String prompt, Model model,
            double temperature) {
        // ANTHROPIC_API_KEY should be set as an environment variable
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();
        try {
            MessageCreateParams.Builder builder = MessageCreateParams.builder()
                    .maxTokens(1024L).addUserMessage(prompt).model(model)
                    .temperature(temperature);
            instructions.ifPresent(builder::system);
            Message response = client.messages().create(builder.build());

            return response.content().stream()
                    .flatMap(contentBlock -> contentBlock.text().stream())
                    .map(textBlock -> textBlock.text())
                    .collect(Collectors.joining());
        } finally {
            client.close();
        }
    }

    void main() {
        String instructions = """
                You are a strict grammar teacher.
                Always respond in one sentence and correct any mistakes.
                """;
        String prompt = "Explain me what is context engineering in simple words";
        Model model = Model.CLAUDE_SONNET_4_20250514;
        double temperature = 0;

        String response = queryModel(Optional.of(instructions), prompt, model,
                temperature);
        System.out.println("=== With system instructions ===");
        System.out.println("User query: " + prompt);
        System.out.println("Response: " + response);

        response = queryModel(Optional.empty(), prompt, model, temperature);
        System.out.println("=== With only user prompt ===");
        System.out.println("User query: " + prompt);
        System.out.println("Response: " + response);
    }

}
