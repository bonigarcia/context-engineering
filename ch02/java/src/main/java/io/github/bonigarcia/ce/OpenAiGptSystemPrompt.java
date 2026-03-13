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

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;
import com.openai.models.chat.completions.ChatCompletionCreateParams.Builder;

public class OpenAiGptSystemPrompt implements AutoCloseable {

    OpenAIClient client;
    ChatModel model;
    double temperature;

    public OpenAiGptSystemPrompt(ChatModel model, float temperature) {
        this.model = model;
        this.temperature = temperature;

        // OPENAI_API_KEY should be set as an environment variable
        client = OpenAIOkHttpClient.fromEnv();
    }

    String queryModel(Optional<String> instructions, String prompt) {
        Builder builder = ChatCompletionCreateParams.builder().model(model)
                .addUserMessage(prompt);
        instructions.ifPresent(builder::addSystemMessage);
        ChatCompletion chatCompletion = client.chat().completions()
                .create(builder.build());
        return chatCompletion.choices().get(0).message().content().get();
    }

    @Override
    public void close() {
        client.close();
    }

    public static void main(String[] args) {
        try (OpenAiGptSystemPrompt demo = new OpenAiGptSystemPrompt(
                ChatModel.GPT_4_1_MINI, 0)) {
            String instructions = """
                    You are a strict grammar teacher.
                    Always respond in one sentence and correct any mistakes.
                    """;
            String prompt = "Explain me what is context engineering in simple words";

            String response = demo.queryModel(Optional.of(instructions),
                    prompt);
            System.out.println("=== With system instructions ===");
            System.out.println("User query: " + prompt);
            System.out.println("Response: " + response);

            response = demo.queryModel(Optional.empty(), prompt);
            System.out.println("=== With only user prompt ===");
            System.out.println("User query: " + prompt);
            System.out.println("Response: " + response);
        }
    }

}