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

public class GoogleGeminiBasic implements AutoCloseable {

    Client client;
    String model;
    float temperature;

    public GoogleGeminiBasic(String model, float temperature) {
        this.model = model;
        this.temperature = temperature;

        // GOOGLE_API_KEY should be set as an environment variable
        client = new Client();
    }

    public String queryModel(String prompt) {
        GenerateContentConfig config = GenerateContentConfig.builder()
                .temperature(temperature).build();
        GenerateContentResponse response = client.models.generateContent(model,
                prompt, config);
        return response.text();
    }

    @Override
    public void close() {
        client.close();
    }

    public static void main(String[] args) {
        try (GoogleGeminiBasic demo = new GoogleGeminiBasic("gemini-2.5-flash",
                0)) {
            String prompt = "How many tokens is your context window?";
            String response = demo.queryModel(prompt);

            System.out.println("User query: " + prompt);
            System.out.println("Response: " + response);
        }
    }

}