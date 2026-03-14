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
import com.google.genai.types.GenerateContentConfig;
import com.google.genai.types.GenerateContentResponse;
import com.google.genai.types.GenerateContentResponseUsageMetadata;
import com.google.genai.types.ThinkingConfig;

public class GoogleGeminiBasic implements AutoCloseable {

    Client client;
    String model;
    float temperature;
    int thinkingBudget;

    public GoogleGeminiBasic(String model, float temperature,
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

        long start = System.nanoTime();
        GenerateContentResponse response = client.models.generateContent(model,
                prompt, config);
        double latency = (System.nanoTime() - start) / 1_000_000_000.0;

        GenerateContentResponseUsageMetadata usage = response.usageMetadata()
                .get();
        System.out.printf("\tLatency: %.3f seconds%n", latency);
        System.out
                .println("\tPrompt tokens: " + usage.promptTokenCount().get());
        System.out.println(
                "\tOutput tokens: " + usage.candidatesTokenCount().get());
        System.out.println(
                "\tThinking tokens: " + usage.thoughtsTokenCount().get());
        System.out.println("\tTotal tokens: " + usage.totalTokenCount().get());

        return response.text();
    }

    @Override
    public void close() {
        client.close();
    }

    public static void main(String[] args) {
        String model = "gemini-2.5-flash";
        float temperature = 0;
        int thinkingBudget = 1024;
        try (GoogleGeminiBasic gemini = new GoogleGeminiBasic(model,
                temperature, thinkingBudget)) {
            String prompt = "How many tokens is your context window?";
            System.out.println("=== Basic model ===");
            System.out.println("User: " + prompt);
            String response = gemini.queryModel(prompt);
            System.out.println("Gemini-2.5: " + response);

            gemini.model = "gemini-3.1-flash-lite-preview";
            gemini.thinkingBudget = 512;
            System.out.println("=== Advanced model  ===");
            System.out.println("User: " + prompt);
            response = gemini.queryModel(prompt);
            System.out.println("Gemini-3.1: " + response);
        }
    }
}