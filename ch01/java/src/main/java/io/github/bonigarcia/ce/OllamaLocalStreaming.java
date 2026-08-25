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
import java.util.Iterator;
import java.util.stream.Stream;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

public class OllamaLocalStreaming {

    static final String DEFAULT_HOST = "http://localhost:11434";
    static final String DEFAULT_MODEL = "gemma3:4b";

    final HttpClient client;
    final ObjectMapper mapper;
    final String host;
    final String model;

    public OllamaLocalStreaming(String host, String model) {
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
        payload.put("stream", true);
        payload.putObject("options").put("temperature", 0);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(host + "/api/generate"))
                .timeout(Duration.ofSeconds(120))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers
                        .ofString(mapper.writeValueAsString(payload)))
                .build();

        long start = System.nanoTime();
        HttpResponse<Stream<String>> response = client.send(request,
                HttpResponse.BodyHandlers.ofLines());

        if (response.statusCode() != 200) {
            throw new IllegalStateException(
                    "Ollama request failed with status "
                            + response.statusCode());
        }

        StringBuilder answer = new StringBuilder();
        JsonNode stats = mapper.createObjectNode();
        double firstToken = -1;

        Iterator<String> lines = response.body().iterator();
        while (lines.hasNext()) {
            String line = lines.next();
            if (line.isBlank()) {
                continue;
            }
            JsonNode chunk = mapper.readTree(line);
            String text = chunk.path("response").asText();
            if (!text.isEmpty() && firstToken < 0) {
                firstToken = (System.nanoTime() - start) / 1_000_000_000.0;
            }
            System.out.print(text);
            System.out.flush();
            answer.append(text);
            if (chunk.path("done").asBoolean()) {
                stats = chunk;
            }
        }
        double latency = (System.nanoTime() - start) / 1_000_000_000.0;
        System.out.println();

        int inputTokens = stats.path("prompt_eval_count").asInt();
        int outputTokens = stats.path("eval_count").asInt();
        double ttft = firstToken < 0 ? latency : firstToken;

        System.out.println("\tModel: " + stats.path("model").asText(model));
        System.out.printf("\tTime to first token: %.3f seconds%n", ttft);
        System.out.printf("\tLatency: %.3f seconds%n", latency);
        System.out.println("\tInput tokens: " + inputTokens);
        System.out.println("\tOutput tokens: " + outputTokens);
        System.out.println("\tTotal tokens: " + (inputTokens + outputTokens));

        return answer.toString().trim();
    }

    static String getEnvOrDefault(String name, String defaultValue) {
        String value = System.getenv(name);
        return value == null || value.isBlank() ? defaultValue : value;
    }

    public static void main(String[] args)
            throws IOException, InterruptedException {
        String host = getEnvOrDefault("OLLAMA_HOST", DEFAULT_HOST);
        String model = getEnvOrDefault("OLLAMA_MODEL", DEFAULT_MODEL);
        OllamaLocalStreaming ollama = new OllamaLocalStreaming(host, model);

        String prompt = "How many tokens are in your context window?";
        System.out.println("User: " + prompt);
        System.out.print("Local LLM: ");
        ollama.queryModel(prompt);
    }

}
