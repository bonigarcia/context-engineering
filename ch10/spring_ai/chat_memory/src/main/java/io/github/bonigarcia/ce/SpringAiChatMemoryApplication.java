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
public class SpringAiChatMemoryApplication {

    private static final String CONVERSATION_ID = "default";

    public static void main(String[] args) {
        SpringApplication.run(SpringAiChatMemoryApplication.class, args);
    }

    @Bean
    ChatMemory chatMemory() {
        return MessageWindowChatMemory.builder()
                .chatMemoryRepository(new InMemoryChatMemoryRepository())
                .maxMessages(10)
                .build();
    }

    @Bean
    CommandLineRunner run(ChatClient.Builder chatClientBuilder, ChatMemory chatMemory) {
        ChatClient chatClient = chatClientBuilder
                .defaultAdvisors(MessageChatMemoryAdvisor.builder(chatMemory).build())
                .build();

        return args -> {
            String prompt1 = "My name is John Snow.";
            String response1 = chatClient.prompt()
                    .advisors(a -> a.param("chat_memory_conversation_id", CONVERSATION_ID))
                    .user(prompt1).call().content();
            System.out.println("User: " + prompt1);
            System.out.println("Model: " + response1);

            String prompt2 = "What is my name?";
            String response2 = chatClient.prompt()
                    .advisors(a -> a.param("chat_memory_conversation_id", CONVERSATION_ID))
                    .user(prompt2).call().content();
            System.out.println("User: " + prompt2);
            System.out.println("Model: " + response2);
        };
    }
}