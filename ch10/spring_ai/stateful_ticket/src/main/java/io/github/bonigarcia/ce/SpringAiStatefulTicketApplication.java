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

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.MessageChatMemoryAdvisor;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.ai.chat.memory.InMemoryChatMemoryRepository;
import org.springframework.ai.chat.memory.MessageWindowChatMemory;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class SpringAiStatefulTicketApplication {

    private static final String CONVERSATION_ID = "session-1";

    public static void main(String[] args) {
        SpringApplication.run(SpringAiStatefulTicketApplication.class, args);
    }

    @Bean
    ChatMemory chatMemory() {
        return MessageWindowChatMemory.builder()
                .chatMemoryRepository(new InMemoryChatMemoryRepository())
                .maxMessages(10).build();
    }

    @Bean
    CommandLineRunner run(ChatClient.Builder builder, ChatMemory chatMemory) {
        ChatClient chatClient = builder
                .defaultSystem("You are a support agent that manages tickets. "
                        + "A ticket has a description and status (open, investigating, resolved). "
                        + "Use the available tools to create and update tickets. "
                        + "Answer concisely.")
                .defaultAdvisors(
                        MessageChatMemoryAdvisor.builder(chatMemory).build())
                .build();

        TicketSystem tickets = new TicketSystem();

        return args -> {
            String[][] dialog = {
                    { "Create a ticket for a broken laptop" },
                    { "I've replaced the screen, it works now" },
                    { "What is the status of my ticket?" },
                    { "Everything is fixed" } };

            for (String[] turn : dialog) {
                String answer = chatClient.prompt()
                        .advisors(a -> a.param(
                                "chat_memory_conversation_id", CONVERSATION_ID))
                        .user(turn[0]).tools(tickets).call().content();
                System.out.println("User: " + turn[0]);
                System.out.println("Model: " + answer);
                System.out.println();
            }
        };
    }

    static class TicketSystem {
        private final Map<Integer, Ticket> tickets = new ConcurrentHashMap<>();
        private final AtomicInteger nextId = new AtomicInteger(1);

        record Ticket(String description, String status) {
            Ticket withStatus(String newStatus) {
                return new Ticket(description, newStatus);
            }
        }

        @Tool(description = "Create a new support ticket")
        String createTicket(
                @ToolParam(description = "Description of the issue") String description) {
            int id = nextId.getAndIncrement();
            tickets.put(id, new Ticket(description, "open"));
            return "Ticket #" + id + " created: \"" + description
                    + "\" (status: open)";
        }

        @Tool(description = "Update the status of an existing ticket")
        String updateStatus(
                @ToolParam(description = "Ticket ID") int ticketId,
                @ToolParam(description = "New status: open, investigating, or resolved") String status) {
            Ticket ticket = tickets.computeIfPresent(ticketId,
                    (k, t) -> t.withStatus(status));
            if (ticket == null) {
                return "Ticket #" + ticketId + " not found.";
            }
            return "Ticket #" + ticketId + " (\"" + ticket.description()
                    + "\") updated to: " + status;
        }

        @Tool(description = "Get the current status of a ticket")
        String getStatus(
                @ToolParam(description = "Ticket ID") int ticketId) {
            Ticket ticket = tickets.get(ticketId);
            if (ticket == null) {
                return "Ticket #" + ticketId + " not found.";
            }
            return "Ticket #" + ticketId + " (\"" + ticket.description()
                    + "\") is currently: " + ticket.status();
        }
    }
}