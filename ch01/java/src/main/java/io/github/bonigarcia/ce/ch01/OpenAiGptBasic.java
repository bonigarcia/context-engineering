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
package io.github.bonigarcia.ce.ch01;

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

class OpenAiGptBasic {

    String queryModel(String prompt) {
        return queryModel(prompt, ChatModel.GPT_4_1_MINI, 0);
    }

    String queryModel(String prompt, ChatModel model, double temperature) {
        // OPENAI_API_KEY should be set as an environment variable
        OpenAIClient client = OpenAIOkHttpClient.fromEnv();

        ResponseCreateParams params = ResponseCreateParams.builder()
                .model(model).input(prompt).temperature(temperature).build();
        Response response = client.responses().create(params);
        return response.output().get(0).asMessage().content().get(0)
                .asOutputText().text();
    }

    void main() {
        String prompt = "How many tokens is your context window?";
        String response = queryModel(prompt);

        System.out.println("User query: " + prompt);
        System.out.println("Response: " + response);
    }

}