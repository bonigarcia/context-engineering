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

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.Reasoning;
import com.openai.models.ReasoningEffort;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.ResponseCreateParams.Builder;

public class OpenAiGptBasic implements AutoCloseable {

    OpenAIClient client;
    ChatModel model;
    double temperature;
    ReasoningEffort reasoning;

    public OpenAiGptBasic(ChatModel model, ReasoningEffort reasoning,
            float temperature) {
        this.model = model;
        this.reasoning = reasoning;
        this.temperature = temperature;

        // OPENAI_API_KEY should be set as an environment variable
        client = OpenAIOkHttpClient.fromEnv();
    }

    public String queryModel(String prompt) {
        Builder modelBuilder = ResponseCreateParams.builder().model(model)
                .input(prompt);
        if (isGpt5OrAbove(model)) {
            modelBuilder
                    .reasoning(Reasoning.builder().effort(reasoning).build());
        } else {
            modelBuilder.temperature(temperature);
        }

        Response response = client.responses().create(modelBuilder.build());
        return response.output().stream()
                .filter(item -> item.message().isPresent())
                .flatMap(item -> item.message().get().content().stream())
                .filter(content -> content.outputText().isPresent())
                .map(content -> content.outputText().get().text())
                .collect(Collectors.joining());
    }

    boolean isGpt5OrAbove(ChatModel model) {
        return model.value().name().matches("GPT_[5-9].*");
    }

    @Override
    public void close() {
        client.close();
    }

    public static void main(String[] args) {
        // Model configuration
        ChatModel model = ChatModel.GPT_5_1;
        ReasoningEffort reasoning = ReasoningEffort.MEDIUM;
        int temperature = 0;

        try (OpenAiGptBasic gpt = new OpenAiGptBasic(model, reasoning,
                temperature)) {
            String prompt = "How many tokens is your context window?";
            String response = gpt.queryModel(prompt);

            System.out.println("User query: " + prompt);
            System.out.println("Response: " + response);
        }
    }

}