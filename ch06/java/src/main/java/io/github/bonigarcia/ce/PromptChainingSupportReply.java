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

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;

public class PromptChainingSupportReply {

    private static final ObjectMapper MAPPER = new ObjectMapper();
    private static final HttpClient HTTP = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(30)).build();
    private static final String API_URL = "https://api.openai.com/v1/chat/completions";
    private final String model;

    public PromptChainingSupportReply(String model) {
        this.model = model;
    }

    public JsonNode extractIssue(String message) throws IOException, InterruptedException {
        ObjectNode body = MAPPER.createObjectNode();
        body.put("model", model);
        body.put("temperature", 0);
        body.set("response_format", MAPPER.createObjectNode().put("type", "json_object"));
        body.set("messages", extractMessages(message));

        JsonNode response = send(body);
        String content = response.path("choices").path(0).path("message").path("content").asText("{}");
        return MAPPER.readTree(content);
    }

    public String draftReply(JsonNode extracted) throws IOException, InterruptedException {
        ObjectNode body = MAPPER.createObjectNode();
        body.put("model", model);
        body.put("temperature", 0.2);
        ArrayNode messages = MAPPER.createArrayNode();
        messages.add(message("system", "You are a support agent. Write a concise reply that acknowledges the issue, summarizes the next step, and stays professional and empathetic."));
        messages.add(message("user", "Use this structured context to draft the reply:\n" + extracted.toPrettyString() + "\n\nWrite 3 to 4 sentences. Do not mention the JSON fields."));
        body.set("messages", messages);

        JsonNode response = send(body);
        return response.path("choices").path(0).path("message").path("content").asText("");
    }

    private ArrayNode extractMessages(String message) {
        ArrayNode messages = MAPPER.createArrayNode();
        messages.add(message("system", "Extract the key support fields from a customer message. Return only valid JSON with the keys product, issue, sentiment, urgency, and next_action."));
        messages.add(message("user", "Customer message:\nThe dashboard keeps logging me out when I switch tabs. I need to sign in again every time."));
        messages.add(message("assistant", supportJson(
                "dashboard",
                "Session expires or resets when switching tabs",
                "frustrated",
                "medium",
                "Check session persistence and browser lifecycle handling.")));
        messages.add(message("user", "Customer message:\n" + message + "\n\nReturn only JSON."));
        return messages;
    }

    private JsonNode send(ObjectNode body) throws IOException, InterruptedException {
        String apiKey = System.getenv("OPENAI_API_KEY");
        if (apiKey == null || apiKey.isBlank()) {
            throw new IllegalStateException("OPENAI_API_KEY is not set");
        }

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(API_URL))
                .timeout(Duration.ofSeconds(90))
                .header("Authorization", "Bearer " + apiKey)
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(MAPPER.writeValueAsString(body)))
                .build();

        HttpResponse<String> response = HTTP.send(request, HttpResponse.BodyHandlers.ofString());
        if (response.statusCode() < 200 || response.statusCode() >= 300) {
            throw new IOException("OpenAI request failed: " + response.statusCode() + " " + response.body());
        }
        return MAPPER.readTree(response.body());
    }

    private ObjectNode message(String role, String content) {
        return MAPPER.createObjectNode().put("role", role).put("content", content);
    }

    private String supportJson(String product, String issue, String sentiment, String urgency, String nextAction) {
        return MAPPER.createObjectNode().put("product", product).put("issue", issue)
                .put("sentiment", sentiment).put("urgency", urgency).put("next_action", nextAction)
                .toString();
    }

    public static void main(String[] args) throws Exception {
        String message = """
                I keep getting signed out of the app whenever I move between dashboard tabs.
                It is happening on both Chrome and Edge, and it is slowing down our team.
                """.strip();

        PromptChainingSupportReply example = new PromptChainingSupportReply(System.getenv().getOrDefault("MODEL", "gpt-4o-mini"));
        JsonNode extracted = example.extractIssue(message);
        String reply = example.draftReply(extracted);

        System.out.println("=== Prompt chaining support reply ===");
        System.out.println("Customer message:");
        System.out.println(message);
        System.out.println("\nStep 1: extracted context");
        System.out.println(MAPPER.writerWithDefaultPrettyPrinter().writeValueAsString(extracted));
        System.out.println("\nStep 2: support reply");
        System.out.println(reply);
    }
}
