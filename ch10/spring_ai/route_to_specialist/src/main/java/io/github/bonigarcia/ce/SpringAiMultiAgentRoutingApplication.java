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
public class SpringAiMultiAgentRoutingApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringAiMultiAgentRoutingApplication.class, args);
    }

    @Bean
    VectorStore vectorStore(EmbeddingModel embeddingModel) {
        return SimpleVectorStore.builder(embeddingModel).build();
    }

    @Bean
    CommandLineRunner run(ChatClient.Builder builder, VectorStore vectorStore) {
        vectorStore.add(List.of(
                new Document(
                        "Password reset: use the self-service portal, then sign in again. "
                                + "Contact HR for escalated requests."),
                new Document(
                        "VPN access: open the local client and choose the office profile. "
                                + "Use your corporate credentials."),
                new Document(
                        "Invoice copy: download the latest invoice from the billing page. "
                                + "Past invoices are archived for 7 years.")));

        ChatClient passwordAgent = builder
                .defaultSystem("You are a password support specialist. "
                        + "Answer concisely using the provided context.")
                .build();

        ChatClient vpnAgent = builder
                .defaultSystem("You are a VPN support specialist. "
                        + "Answer concisely using the provided context.")
                .build();

        ChatClient invoiceAgent = builder
                .defaultSystem("You are an invoice support specialist. "
                        + "Answer concisely using the provided context.")
                .build();

        ChatClient supervisor = builder
                .defaultSystem("You are a triage agent. Route each question to "
                        + "the right specialist and relay their answer to the user.")
                .build();

        RouterTool router = new RouterTool(vectorStore, passwordAgent, vpnAgent,
                invoiceAgent);

        return args -> {
            String[] questions = {
                    "How do I reset my password?",
                    "How do I connect to the VPN?",
                    "Can I get a copy of my last invoice?" };

            for (String question : questions) {
                String answer = supervisor.prompt()
                        .user(question).tools(router).call().content();
                System.out.println("User: " + question);
                System.out.println("Model: " + answer);
                System.out.println();
            }
        };
    }

    static class RouterTool {
        private final VectorStore vectorStore;
        private final ChatClient passwordAgent;
        private final ChatClient vpnAgent;
        private final ChatClient invoiceAgent;

        RouterTool(VectorStore vectorStore, ChatClient passwordAgent,
                ChatClient vpnAgent, ChatClient invoiceAgent) {
            this.vectorStore = vectorStore;
            this.passwordAgent = passwordAgent;
            this.vpnAgent = vpnAgent;
            this.invoiceAgent = invoiceAgent;
        }

        @Tool(description = "Route a support question to the right specialist team")
        String routeToSpecialist(
                @ToolParam(description = "Category: 'password', 'vpn', or 'invoice'") String category,
                @ToolParam(description = "The user's question") String question) {
            List<Document> docs = vectorStore.similaritySearch(
                    SearchRequest.builder().query(question).topK(2).build());
            String context = docs.stream().map(Document::getText)
                    .collect(Collectors.joining("\n"));

            ChatClient specialist = switch (category) {
                case "password" -> passwordAgent;
                case "vpn" -> vpnAgent;
                case "invoice" -> invoiceAgent;
                default -> throw new IllegalArgumentException(
                        "Unknown category: " + category);
            };

            return specialist.prompt()
                    .user("Context:\n" + context + "\n\nQuestion: " + question)
                    .call().content();
        }
    }

}