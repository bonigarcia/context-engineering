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

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.vectorstore.QuestionAnswerAdvisor;
import org.springframework.ai.document.Document;
import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.vectorstore.SimpleVectorStore;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class SpringAiRagRetrievalApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringAiRagRetrievalApplication.class, args);
    }

    @Bean
    VectorStore vectorStore(EmbeddingModel embeddingModel) {
        return SimpleVectorStore.builder(embeddingModel).build();
    }

    @Bean
    CommandLineRunner run(ChatClient.Builder chatClientBuilder, VectorStore vectorStore) {
        vectorStore.add(List.of(
                new Document("Reset password: use the self-service portal, then sign in again."),
                new Document("VPN access: open the local client and choose the office profile."),
                new Document("Invoice copy: download the latest invoice from the billing page.")));

        ChatClient chatClient = chatClientBuilder.build();

        return args -> {
            String answer = chatClient.prompt()
                    .advisors(QuestionAnswerAdvisor.builder(vectorStore).build())
                    .user("How do I reset my password?")
                    .call()
                    .content();

            System.out.println(answer);
        };
    }
}
