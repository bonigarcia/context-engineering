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
package io.github.bonigarcia.ce.ch02;

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

public class PromptStuffing {

    private static final String QUESTION = """
            According to the article, what are the three main challenges of
            context engineering, and how are they described?
            """;

    private static final String ARTICLE = """
            [Article: Internal note on context engineering]

            Context engineering is the discipline of shaping and managing all the
            information that an AI model receives at inference time. Instead of
            treating a prompt as a single flat string, context engineering views
            the model's input as a deliberately assembled mix of complementary
            components: system instructions, user request, external knowledge,
            tools, memory, and state.

            The first challenge is relevance. Because the context window is
            limited, engineers must decide which pieces of information are
            genuinely useful for solving the current task and which are noise.
            Overstuffing the prompt with loosely related details can dilute the
            model's attention and lead to generic or confused answers.

            The second challenge is freshness. The model's parametric memory is
            frozen at training time, so external knowledge and memory pipelines
            must continuously feed updated information into the context window.
            This includes recent documents, user preferences, and live signals
            from tools or sensors.

            The third challenge is structure. Raw text is often messy; effective
            context engineering requires predictable patterns such as templates,
            sections, and schemas. Well-structured context makes it easier for
            the model to understand roles, goals, constraints, and how retrieved
            evidence should be used.

            In short, context engineering is about giving the model exactly the
            right information, in the right format, at the right moment—no more
            and no less.
            """;

    public static void main(String[] args) {
        // Ensure OPENAI_API_KEY is set in your environment
        OpenAIClient client = OpenAIOkHttpClient.fromEnv();

        runWithoutStuffedContext(client);
        runWithStuffedContext(client);
    }

    private static void runWithoutStuffedContext(OpenAIClient client) {
        System.out.println("1) Asking without stuffed article");

        String userPrompt = QUESTION;
        String response = askModel(client, userPrompt);
        System.out.println(response);
    }

    private static void runWithStuffedContext(OpenAIClient client) {
        System.out.println("2) Asking with stuffed article as context");

        String stuffedPrompt = """
                You are a helpful assistant. I will give you an article between
                <article> and </article>. Then I will ask you a question.
                You must answer ONLY using information from the article.

                <article>
                %s
                </article>

                Question: %s
                """.formatted(ARTICLE, QUESTION);

        String response = askModel(client, stuffedPrompt);
        System.out.println(response);
    }

    private static String askModel(OpenAIClient client, String userMessage) {
        String systemMessage = """
                You are a careful assistant. If you do not have enough information, say
                'I don't know based on the context I have.'""";
        ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                .model(ChatModel.GPT_4O).addSystemMessage(systemMessage)
                .addUserMessage(userMessage).build();
        ChatCompletion completion = client.chat().completions().create(params);
        return completion.choices().get(0).message().content().get();
    }

}
