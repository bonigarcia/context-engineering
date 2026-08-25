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

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.core.http.StreamResponse;
import com.anthropic.helpers.MessageAccumulator;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;
import com.anthropic.models.messages.Model;
import com.anthropic.models.messages.RawMessageStreamEvent;
import com.anthropic.models.messages.Usage;

public class AnthropicClaudeStreaming implements AutoCloseable {

    AnthropicClient client;
    Model model;
    long maxTokens;
    double temperature;

    public AnthropicClaudeStreaming(Model model, long maxTokens,
            float temperature) {
        this.model = model;
        this.maxTokens = maxTokens;
        this.temperature = temperature;

        // ANTHROPIC_API_KEY should be set as an environment variable
        client = AnthropicOkHttpClient.fromEnv();
    }

    public String queryModel(String prompt) {
        MessageCreateParams params = MessageCreateParams.builder().model(model)
                .maxTokens(maxTokens).temperature(temperature)
                .addUserMessage(prompt).build();

        StringBuilder answer = new StringBuilder();
        MessageAccumulator accumulator = MessageAccumulator.create();
        long start = System.nanoTime();
        double[] firstToken = { -1 };

        try (StreamResponse<RawMessageStreamEvent> stream = client.messages()
                .createStreaming(params)) {
            stream.stream().peek(accumulator::accumulate)
                    .flatMap(event -> event.contentBlockDelta().stream())
                    .flatMap(delta -> delta.delta().text().stream())
                    .forEach(text -> {
                        if (firstToken[0] < 0) {
                            firstToken[0] = (System.nanoTime() - start)
                                    / 1_000_000_000.0;
                        }
                        System.out.print(text.text());
                        System.out.flush();
                        answer.append(text.text());
                    });
        }
        double latency = (System.nanoTime() - start) / 1_000_000_000.0;
        System.out.println();

        Message message = accumulator.message();
        Usage usage = message.usage();
        double ttft = firstToken[0] < 0 ? latency : firstToken[0];

        System.out.println("\tModel: " + message.model());
        System.out.printf("\tTime to first token: %.3f seconds%n", ttft);
        System.out.printf("\tLatency: %.3f seconds%n", latency);
        System.out.println("\tInput tokens: " + usage.inputTokens());
        System.out.println("\tOutput tokens: " + usage.outputTokens());

        return answer.toString().trim();
    }

    @Override
    public void close() {
        client.close();
    }

    public static void main(String[] args) {
        try (AnthropicClaudeStreaming claude = new AnthropicClaudeStreaming(
                Model.CLAUDE_HAIKU_4_5, 2048, 0)) {
            String prompt = "How many tokens are in your context window?";
            System.out.println("User: " + prompt);
            System.out.print("Claude: ");
            claude.queryModel(prompt);
        }
    }

}
