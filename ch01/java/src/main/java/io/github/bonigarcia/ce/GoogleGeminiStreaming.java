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

import com.google.genai.Client;
import com.google.genai.ResponseStream;
import com.google.genai.types.GenerateContentConfig;
import com.google.genai.types.GenerateContentResponse;
import com.google.genai.types.GenerateContentResponseUsageMetadata;
import com.google.genai.types.ThinkingConfig;

public class GoogleGeminiStreaming implements AutoCloseable {

    Client client;
    String model;
    float temperature;
    int thinkingBudget;

    public GoogleGeminiStreaming(String model, float temperature,
            int thinkingBudget) {
        this.model = model;
        this.temperature = temperature;
        this.thinkingBudget = thinkingBudget;

        // GOOGLE_API_KEY should be set as an environment variable
        client = new Client();
    }

    public String queryModel(String prompt) {
        GenerateContentConfig config = GenerateContentConfig.builder()
                .temperature(temperature).thinkingConfig(ThinkingConfig
                        .builder().thinkingBudget(thinkingBudget).build())
                .build();

        StringBuilder answer = new StringBuilder();
        GenerateContentResponseUsageMetadata usage = null;
        long start = System.nanoTime();
        double firstToken = -1;

        try (ResponseStream<GenerateContentResponse> stream = client.models
                .generateContentStream(model, prompt, config)) {
            for (GenerateContentResponse chunk : stream) {
                if (chunk.usageMetadata().isPresent()) {
                    usage = chunk.usageMetadata().get();
                }
                String text = chunk.text();
                if (text == null || text.isEmpty()) {
                    continue;
                }
                if (firstToken < 0) {
                    firstToken = (System.nanoTime() - start) / 1_000_000_000.0;
                }
                System.out.print(text);
                System.out.flush();
                answer.append(text);
            }
        }
        double latency = (System.nanoTime() - start) / 1_000_000_000.0;
        System.out.println();

        double ttft = firstToken < 0 ? latency : firstToken;
        System.out.printf("\tTime to first token: %.3f seconds%n", ttft);
        System.out.printf("\tLatency: %.3f seconds%n", latency);
        if (usage != null) {
            System.out.println(
                    "\tPrompt tokens: " + usage.promptTokenCount().get());
            System.out.println(
                    "\tOutput tokens: " + usage.candidatesTokenCount().get());
            System.out.println(
                    "\tThinking tokens: " + usage.thoughtsTokenCount().get());
            System.out.println(
                    "\tTotal tokens: " + usage.totalTokenCount().get());
        }

        return answer.toString().trim();
    }

    @Override
    public void close() {
        client.close();
    }

    public static void main(String[] args) {
        try (GoogleGeminiStreaming gemini = new GoogleGeminiStreaming(
                "gemini-2.5-flash", 0, 512)) {
            String prompt = "How many tokens are in your context window?";
            System.out.println("User: " + prompt);
            System.out.print("Gemini: ");
            gemini.queryModel(prompt);
        }
    }

}
