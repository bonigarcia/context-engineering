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

import com.google.genai.Client;
import com.google.genai.types.Content;
import com.google.genai.types.GenerateContentConfig;
import com.google.genai.types.GenerateContentResponse;
import com.google.genai.types.Part;

public class GoogleGeminiSystemPrompt {

    String queryModel(Optional<String> instructions, String prompt,
            String model, float temperature) {
        // GOOGLE_API_KEY should be set as an environment variable
        try (Client client = new Client()) {
            GenerateContentConfig.Builder builder = GenerateContentConfig
                    .builder().temperature(temperature);
            instructions.ifPresent(i -> builder
                    .systemInstruction(Content.fromParts(Part.fromText(i))));
            GenerateContentResponse response = client.models
                    .generateContent(model, prompt, builder.build());
            return response.text();
        }
    }

    void main() {
        String instructions = """
                You are a strict grammar teacher.
                Always respond in one sentence and correct any mistakes.
                """;
        String prompt = "Explain me what is context engineering in simple words";
        String model = "gemini-2.5-flash";
        float temperature = 0;

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
