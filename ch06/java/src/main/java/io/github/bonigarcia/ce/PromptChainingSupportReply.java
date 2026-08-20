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

    public JsonNode analyzeInquiry(String message) throws IOException, InterruptedException {
        ObjectNode body = MAPPER.createObjectNode();
        body.put("model", model);
        body.put("temperature", 0);
        body.set("response_format", MAPPER.createObjectNode().put("type", "json_object"));

        ArrayNode messages = MAPPER.createArrayNode();
        messages.add(message("system",
                "Analyze the customer support inquiry. Return only valid JSON with the following keys: "
                        + "category (one of: billing, technical_bug, feature_request, general_inquiry), "
                        + "urgency (one of: low, medium, high, critical), "
                        + "sentiment (one of: positive, neutral, frustrated, angry), "
                        + "summary (a concise 1-sentence summary of the core issue)."));
        messages.add(message("user", "Customer inquiry:\n" + message + "\n\nReturn only JSON."));
        body.set("messages", messages);

        JsonNode response = send(body);
        String content = response.path("choices").path(0).path("message").path("content").asText("{}");
        return MAPPER.readTree(content);
    }

    public JsonNode resolvePolicy(JsonNode analysis) {
        String category = analysis.path("category").asText("general_inquiry");
        String urgency = analysis.path("urgency").asText("medium");

        ObjectNode policy = MAPPER.createObjectNode();
        if ("billing".equals(category) && ("high".equals(urgency) || "critical".equals(urgency))) {
            policy.put("sla_response_time", "1 hour");
            policy.put("escalation_team", "Priority Billing & Finance Ops");
            policy.put("resolution_guidelines",
                    "Acknowledge the billing discrepancy, confirm expedited review with Finance Ops for refund processing, and provide a direct case tracking reference.");
        } else if ("technical_bug".equals(category) && ("high".equals(urgency) || "critical".equals(urgency))) {
            policy.put("sla_response_time", "2 hours");
            policy.put("escalation_team", "Tier-2 Engineering");
            policy.put("resolution_guidelines",
                    "Acknowledge the technical disruption, outline immediate diagnostic steps, and route logs to Tier-2 Engineering.");
        } else {
            policy.put("sla_response_time", "24 hours");
            policy.put("escalation_team", "Standard Support");
            policy.put("resolution_guidelines",
                    "Provide helpful guidance addressing the customer question and offer links to documentation.");
        }
        return policy;
    }

    public String draftReply(String message, JsonNode analysis, JsonNode policy) throws IOException, InterruptedException {
        String contextPrompt = """
                Customer inquiry:
                %s

                Case analysis:
                - Category: %s
                - Urgency: %s
                - Customer sentiment: %s
                - Core issue: %s

                Resolution policy:
                - Target SLA response: %s
                - Assigned team: %s
                - Guidelines: %s

                Draft a professional, empathetic 3 to 4 sentence customer reply adhering to the resolution policy.
                """.formatted(
                message,
                analysis.path("category").asText(),
                analysis.path("urgency").asText(),
                analysis.path("sentiment").asText(),
                analysis.path("summary").asText(),
                policy.path("sla_response_time").asText(),
                policy.path("escalation_team").asText(),
                policy.path("resolution_guidelines").asText()
        );

        ObjectNode body = MAPPER.createObjectNode();
        body.put("model", model);
        body.put("temperature", 0.2);

        ArrayNode messages = MAPPER.createArrayNode();
        messages.add(message("system",
                "You are an enterprise customer support specialist. Write a professional, empathetic reply "
                        + "that strictly follows the provided resolution policy and case analysis. "
                        + "Do not mention JSON keys or internal system labels."));
        messages.add(message("user", contextPrompt));
        body.set("messages", messages);

        JsonNode response = send(body);
        return response.path("choices").path(0).path("message").path("content").asText("");
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

    public static void main(String[] args) throws Exception {
        String message = """
                We were double-billed on invoice #INV-9821 for our annual Enterprise tier ($4,800 instead of $2,400).
                This is blocking our quarterly accounting close, and we need an immediate refund and an updated invoice.
                """.strip();

        PromptChainingSupportReply example = new PromptChainingSupportReply(
                System.getenv().getOrDefault("MODEL", "gpt-4o-mini"));
        JsonNode analysis = example.analyzeInquiry(message);
        JsonNode policy = example.resolvePolicy(analysis);
        String reply = example.draftReply(message, analysis, policy);

        System.out.println("=== Prompt chaining support reply ===");
        System.out.println("Customer message:");
        System.out.println(message);
        System.out.println("\nStep 1: extracted analysis");
        System.out.println(MAPPER.writerWithDefaultPrettyPrinter().writeValueAsString(analysis));
        System.out.println("\nIntermediate: resolved policy");
        System.out.println(MAPPER.writerWithDefaultPrettyPrinter().writeValueAsString(policy));
        System.out.println("\nStep 2: customer reply");
        System.out.println(reply);
    }
}
