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
import org.springframework.ai.document.Document;
import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.SimpleVectorStore;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Counter;

@SpringBootApplication
public class SpringAiObservabilityApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringAiObservabilityApplication.class, args);
    }

    @Bean
    VectorStore vectorStore(EmbeddingModel embeddingModel) {
        return SimpleVectorStore.builder(embeddingModel).build();
    }

    @Bean
    CommandLineRunner run(ChatClient.Builder builder, VectorStore vectorStore,
            MeterRegistry meterRegistry) {
        vectorStore.add(List.of(
                new Document(
                        "Password reset: use the self-service portal, then sign in again."),
                new Document(
                        "VPN access: open the local client and choose the office profile.")));

        ChatClient chatClient = builder
                .defaultSystem("You are a helpful IT support assistant. "
                        + "Answer concisely using the provided context.")
                .build();

        Counter retrievalCounter = Counter.builder("context.retrievals")
                .description("Number of vector store retrievals").register(
                        meterRegistry);

        return args -> {
            String question = "How do I reset my password?";
            List<Document> docs = vectorStore.similaritySearch(
                    SearchRequest.builder().query(question).topK(2).build());
            retrievalCounter.increment();

            String context = docs.stream().map(Document::getText)
                    .collect(Collectors.joining("\n"));

            String answer = chatClient.prompt()
                    .user("Context:\n" + context + "\n\nQuestion: " + question)
                    .call().content();

            System.out.println("User: " + question);
            System.out.println("Model: " + answer);
            System.out.println("---");
            System.out.println("Custom metric 'context.retrievals': "
                    + (int) retrievalCounter.count());
            System.out.println("--- Available Micrometer metrics:");
            meterRegistry.getMeters().forEach(m -> System.out.println(
                    "  " + m.getId().getName() + " = " + m.measure()
                            .iterator().next().getValue()));
            System.out.println("---");
        };
    }
}