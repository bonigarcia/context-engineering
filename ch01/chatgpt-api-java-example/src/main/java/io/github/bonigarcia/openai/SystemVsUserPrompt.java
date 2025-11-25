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
package io.github.bonigarcia.openai;

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

public class SystemVsUserPrompt {

    public static void main(String[] args) {
        // Ensure OPENAI_API_KEY is set in your environment
        OpenAIClient client = OpenAIOkHttpClient.fromEnv();

        String systemMessage = """
                You are a strict grammar teacher.
                Always respond in one sentence and correct any mistakes.
                """;
        String userPrompt = "Explain me what is context engineering in simple words";

        // Example 1: Using a system message for high-level behavior
        ChatCompletionCreateParams systemPromptParams = ChatCompletionCreateParams
                .builder().model(ChatModel.GPT_4_1)
                .addSystemMessage(systemMessage).addUserMessage(userPrompt)
                .build();
        ChatCompletion systemPromptCompletion = client.chat().completions()
                .create(systemPromptParams);
        String systemPromptAnswer = systemPromptCompletion.choices().get(0)
                .message().content().get();
        System.out.println("=== With system instructions ===");
        System.out.println(systemPromptAnswer);
        System.out.println();

        // Example 2: No system message, everything in the user prompt
        ChatCompletionCreateParams userPromptParams = ChatCompletionCreateParams
                .builder().model(ChatModel.GPT_4_1).addUserMessage(userPrompt)
                .build();
        ChatCompletion userPromptCompletion = client.chat().completions()
                .create(userPromptParams);
        String userPromptAnswer = userPromptCompletion.choices().get(0)
                .message().content().get();
        System.out.println("=== With only user prompt ===");
        System.out.println(userPromptAnswer);
    }
}
