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

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.MessageChatMemoryAdvisor;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.ai.chat.memory.InMemoryChatMemoryRepository;
import org.springframework.ai.chat.memory.MessageWindowChatMemory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class SpringAiContextCompressionApplication {

    private static final String CONVERSATION_ID = "default";

    public static void main(String[] args) {
        SpringApplication.run(SpringAiContextCompressionApplication.class, args);
    }

    @Bean
    ChatMemory chatMemory() {
        return MessageWindowChatMemory.builder()
                .chatMemoryRepository(new InMemoryChatMemoryRepository())
                .maxMessages(20).build();
    }

    @Bean
    CommandLineRunner run(ChatClient.Builder builder, ChatMemory chatMemory) {
        ChatClient chatClient = builder
                .defaultSystem("You are a helpful assistant. Answer concisely. "
                        + "Before each response, compress the conversation history "
                        + "into a short summary that preserves all key facts "
                        + "(names, preferences, past questions). "
                        + "Then answer the user based on that summary.")
                .defaultAdvisors(
                        MessageChatMemoryAdvisor.builder(chatMemory).build())
                .build();

        String[][] dialog = {
                { "Hi, my name is Alice and I work in finance" },
                { "I need help with the quarterly report" },
                { "The pivot table won't refresh" },
                { "Actually I think it's a permissions thing" },
                { "What was my first question and what department am I in?" } };

        return args -> {
            for (String[] turn : dialog) {
                String answer = chatClient.prompt()
                        .advisors(a -> a.param(
                                "chat_memory_conversation_id", CONVERSATION_ID))
                        .user(turn[0]).call().content();
                System.out.println("User: " + turn[0]);
                System.out.println("Model: " + answer);
                System.out.println();
            }
        };
    }
}