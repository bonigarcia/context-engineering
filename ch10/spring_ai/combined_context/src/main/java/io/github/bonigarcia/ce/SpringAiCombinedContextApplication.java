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

import java.util.List;
import java.util.stream.Collectors;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.MessageChatMemoryAdvisor;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.ai.chat.memory.InMemoryChatMemoryRepository;
import org.springframework.ai.chat.memory.MessageWindowChatMemory;
import org.springframework.ai.document.Document;
import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.SimpleVectorStore;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class SpringAiCombinedContextApplication {

    private static final String CONVERSATION_ID = "default";

    public static void main(String[] args) {
        SpringApplication.run(SpringAiCombinedContextApplication.class, args);
    }

    @Bean
    ChatMemory chatMemory() {
        return MessageWindowChatMemory.builder()
                .chatMemoryRepository(new InMemoryChatMemoryRepository())
                .maxMessages(10)
                .build();
    }

    @Bean
    VectorStore vectorStore(EmbeddingModel embeddingModel) {
        return SimpleVectorStore.builder(embeddingModel).build();
    }

    @Bean
    CommandLineRunner run(ChatClient.Builder chatClientBuilder, ChatMemory chatMemory,
            VectorStore vectorStore) {
        vectorStore.add(List.of(
                new Document("VPN access: open the local client and choose the office profile."),
                new Document(
                        "Password reset: use the self-service portal, then sign in again."),
                new Document(
                        "Invoice copy: download the latest invoice from the billing page.")));

        ChatClient chatClient = chatClientBuilder
                .defaultSystem("You are a helpful IT support assistant. "
                        + "Answer concisely using the provided context.")
                .defaultAdvisors(MessageChatMemoryAdvisor.builder(chatMemory).build())
                .build();

        return args -> {
            String question1 = "How do I reset my password?";
            List<Document> docs = vectorStore.similaritySearch(
                    SearchRequest.builder().query(question1).topK(2).build());
            String context = docs.stream().map(Document::getText)
                    .collect(Collectors.joining("\n"));
            String answer1 = chatClient.prompt()
                    .advisors(a -> a.param("chat_memory_conversation_id", CONVERSATION_ID))
                    .user("Context:\n" + context + "\n\nQuestion: " + question1).call()
                    .content();
            System.out.println("User: " + question1);
            System.out.println("Model: " + answer1);

            String question2 = "What is 12 + 30?";
            String answer2 = chatClient.prompt()
                    .advisors(a -> a.param("chat_memory_conversation_id", CONVERSATION_ID))
                    .tools(new ItTools())
                    .user(question2).call().content();
            System.out.println("User: " + question2);
            System.out.println("Model: " + answer2);

            String question3 = "What was my first question?";
            String answer3 = chatClient.prompt()
                    .advisors(a -> a.param("chat_memory_conversation_id", CONVERSATION_ID))
                    .user(question3).call().content();
            System.out.println("User: " + question3);
            System.out.println("Model: " + answer3);
        };
    }

    static class ItTools {
        @Tool(description = "Add two whole numbers and return the sum")
        int add(
                @ToolParam(description = "first whole number") int a,
                @ToolParam(description = "second whole number") int b) {
            return a + b;
        }
    }
}