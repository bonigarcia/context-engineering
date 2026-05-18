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
import java.util.List;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;

public class FewShotTicketNormalizer {

    private static final ObjectMapper MAPPER = new ObjectMapper();
    private static final HttpClient HTTP = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(30)).build();
    private static final String API_URL = "https://api.openai.com/v1/chat/completions";
    private final String model;

    public FewShotTicketNormalizer(String model) {
        this.model = model;
    }

    public JsonNode normalizeReport(String report) throws IOException, InterruptedException {
        ObjectNode body = MAPPER.createObjectNode();
        body.put("model", model);
        body.put("temperature", 0);
        body.set("response_format", MAPPER.createObjectNode().put("type", "json_object"));
        body.set("messages", buildMessages(report));

        JsonNode response = send(body);
        String content = response.path("choices").path(0).path("message").path("content").asText("{}");
        return MAPPER.readTree(content);
    }

    private ArrayNode buildMessages(String report) {
        ArrayNode messages = MAPPER.createArrayNode();
        messages.add(message("system", "You normalize bug reports into compact support tickets. Return only valid JSON with the keys title, category, priority, summary, and next_step."));
        messages.add(message("user", "Bug report:\nThe mobile app crashes when I try to upload a 20 MB PDF. It worked yesterday."));
        messages.add(message("assistant", ticketJson(
                "Crash when uploading large PDF",
                "file_upload",
                "high",
                "The mobile app crashes during PDF upload when the file is around 20 MB.",
                "Investigate upload limits and crash logs for the mobile client.")));
        messages.add(message("user", "Bug report:\nSearch results on the dashboard take a long time to load, especially in the morning."));
        messages.add(message("assistant", ticketJson(
                "Slow dashboard search",
                "performance",
                "medium",
                "Dashboard search becomes slow, with the issue being most visible during morning usage.",
                "Check query latency, indexing, and peak-time load on the search service.")));
        messages.add(message("user", "Bug report:\n" + report + "\n\nReturn only JSON."));
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

    private String ticketJson(String title, String category, String priority, String summary, String nextStep) {
        return MAPPER.createObjectNode().put("title", title).put("category", category)
                .put("priority", priority).put("summary", summary).put("next_step", nextStep)
                .toString();
    }

    public static void main(String[] args) throws Exception {
        String report = """
                The app logs me out whenever I close the browser tab.
                I already checked the password manager, and I have to sign in every time.
                """.strip();

        FewShotTicketNormalizer normalizer = new FewShotTicketNormalizer(System.getenv().getOrDefault("MODEL", "gpt-4o-mini"));
        JsonNode ticket = normalizer.normalizeReport(report);

        System.out.println("=== Few-shot ticket normalizer ===");
        System.out.println("Bug report:");
        System.out.println(report);
        System.out.println("\nNormalized ticket:");
        System.out.println(MAPPER.writerWithDefaultPrettyPrinter().writeValueAsString(ticket));
    }
}
