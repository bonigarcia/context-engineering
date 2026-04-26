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
import com.fasterxml.jackson.databind.node.ObjectNode;

public class OllamaLocalBasic {

    static final String DEFAULT_HOST = "http://localhost:11434";
    static final String DEFAULT_MODEL = "gemma3:4b";

    final HttpClient client;
    final ObjectMapper mapper;
    final String host;
    final String model;

    public OllamaLocalBasic(String host, String model) {
        this.client = HttpClient.newHttpClient();
        this.mapper = new ObjectMapper();
        this.host = host;
        this.model = model;
    }

    public String queryModel(String prompt)
            throws IOException, InterruptedException {
        ObjectNode payload = mapper.createObjectNode();
        payload.put("model", model);
        payload.put("prompt", prompt);
        payload.put("stream", false);
        payload.putObject("options").put("temperature", 0);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(host + "/api/generate"))
                .timeout(Duration.ofSeconds(120))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers
                        .ofString(mapper.writeValueAsString(payload)))
                .build();

        long start = System.nanoTime();
        HttpResponse<String> response = client.send(request,
                HttpResponse.BodyHandlers.ofString());
        double latency = (System.nanoTime() - start) / 1_000_000_000.0;

        if (response.statusCode() != 200) {
            throw new IllegalStateException(
                    "Ollama request failed: " + response.body());
        }

        JsonNode result = mapper.readTree(response.body());
        int inputTokens = result.path("prompt_eval_count").asInt();
        int outputTokens = result.path("eval_count").asInt();

        System.out.println("\tModel: " + result.path("model").asText(model));
        System.out.printf("\tLatency: %.3f seconds%n", latency);
        System.out.println("\tInput tokens: " + inputTokens);
        System.out.println("\tOutput tokens: " + outputTokens);
        System.out.println("\tTotal tokens: " + (inputTokens + outputTokens));

        return result.path("response").asText().trim();
    }

    static String getEnvOrDefault(String name, String defaultValue) {
        String value = System.getenv(name);
        return value == null || value.isBlank() ? defaultValue : value;
    }

    public static void main(String[] args)
            throws IOException, InterruptedException {
        String host = getEnvOrDefault("OLLAMA_HOST", DEFAULT_HOST);
        String model = getEnvOrDefault("OLLAMA_MODEL", DEFAULT_MODEL);
        OllamaLocalBasic ollama = new OllamaLocalBasic(host, model);

        String prompt = "How many tokens is your context window?";
        System.out.println("User: " + prompt);
        String response = ollama.queryModel(prompt);
        System.out.println("Local LLM: " + response);
    }

}
