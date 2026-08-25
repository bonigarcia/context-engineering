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

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.core.http.StreamResponse;
import com.openai.helpers.ResponseAccumulator;
import com.openai.models.ChatModel;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.ResponseStreamEvent;
import com.openai.models.responses.ResponseUsage;

public class OpenAiGptStreaming implements AutoCloseable {

    OpenAIClient client;
    ChatModel model;
    double temperature;

    public OpenAiGptStreaming(ChatModel model, float temperature) {
        this.model = model;
        this.temperature = temperature;

        // OPENAI_API_KEY should be set as an environment variable
        client = OpenAIOkHttpClient.fromEnv();
    }

    public String queryModel(String prompt) {
        ResponseCreateParams params = ResponseCreateParams.builder()
                .model(model).input(prompt).temperature(temperature).build();

        StringBuilder answer = new StringBuilder();
        ResponseAccumulator accumulator = ResponseAccumulator.create();
        long start = System.nanoTime();
        double[] firstToken = { -1 };

        try (StreamResponse<ResponseStreamEvent> stream = client.responses()
                .createStreaming(params)) {
            stream.stream().peek(accumulator::accumulate)
                    .flatMap(event -> event.outputTextDelta().stream())
                    .forEach(event -> {
                        if (firstToken[0] < 0) {
                            firstToken[0] = (System.nanoTime() - start)
                                    / 1_000_000_000.0;
                        }
                        System.out.print(event.delta());
                        System.out.flush();
                        answer.append(event.delta());
                    });
        }
        double latency = (System.nanoTime() - start) / 1_000_000_000.0;
        System.out.println();

        Response response = accumulator.response();
        ResponseUsage usage = response.usage().get();
        double ttft = firstToken[0] < 0 ? latency : firstToken[0];

        System.out.println("\tModel: " + response.model().chat().get());
        System.out.printf("\tTime to first token: %.3f seconds%n", ttft);
        System.out.printf("\tLatency: %.3f seconds%n", latency);
        System.out.println("\tInput tokens: " + usage.inputTokens());
        System.out.println("\tOutput tokens: " + usage.outputTokens());
        System.out.println("\tTotal tokens: " + usage.totalTokens());

        return answer.toString().trim();
    }

    @Override
    public void close() {
        client.close();
    }

    public static void main(String[] args) {
        try (OpenAiGptStreaming gpt = new OpenAiGptStreaming(
                ChatModel.GPT_4O_MINI, 0)) {
            String prompt = "How many tokens are in your context window?";
            System.out.println("User: " + prompt);
            System.out.print("AI: ");
            gpt.queryModel(prompt);
        }
    }

}
