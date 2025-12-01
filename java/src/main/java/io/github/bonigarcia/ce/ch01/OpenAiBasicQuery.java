/*
 * (C) Copyright 2025 Boni Garcia (https://bonigarcia.github.io/)
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

public class OpenAiBasicQuery {

    public static void main(String[] args) {
        // Ensure OPENAI_API_KEY is set in your environment
        OpenAIClient client = OpenAIOkHttpClient.fromEnv();

        String prompt = "How many tokens is your context window?";
        ResponseCreateParams params = ResponseCreateParams.builder()
                .input(prompt).model(ChatModel.GPT_4_1).build();
        Response response = client.responses().create(params);
        String output = response.output().get(0).asMessage().content().get(0)
                .asOutputText().text();

        System.out.println("User query: " + prompt);
        System.out.println("Response: " + output);
    }

}