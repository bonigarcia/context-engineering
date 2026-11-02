/*
(C) Copyright 2026 Boni Garcia (https://bonigarcia.github.io/)
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
package io.github.bonigarcia.ce;

import com.fasterxml.jackson.annotation.JsonClassDescription;
import com.fasterxml.jackson.annotation.JsonPropertyDescription;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.ResponseFunctionToolCall;
import com.openai.models.responses.ResponseInputItem;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public final class FunctionCalling {

    private FunctionCalling() {
    }

    @JsonClassDescription("Gets the current weather in a location.")
    static class GetWeather {

        @JsonPropertyDescription("Location to look up.")
        public String location;

        public Map<String, Object> execute() {
            String key = location.trim().toLowerCase();

            return switch (key) {
                case "san francisco" -> Map.of(
                        "location", "San Francisco",
                        "temperature_c", 18,
                        "condition", "Sunny",
                        "humidity_percent", 63);
                case "new york" -> Map.of(
                        "location", "New York",
                        "temperature_c", 12,
                        "condition", "Cloudy",
                        "humidity_percent", 71);
                case "london" -> Map.of(
                        "location", "London",
                        "temperature_c", 10,
                        "condition", "Light rain",
                        "humidity_percent", 82);
                default -> Map.of(
                        "location", location,
                        "temperature_c", 21,
                        "condition", "Unknown (demo data)",
                        "humidity_percent", 50);
            };
        }
    }

    public static void main(String[] args) {
        OpenAIClient client = OpenAIOkHttpClient.fromEnv();

        String prompt = "What is the weather in San Francisco?";
        System.out.println("User: " + prompt);

        List<ResponseInputItem> inputs = new ArrayList<>();
        inputs.add(ResponseInputItem.ofMessage(ResponseInputItem.Message.builder()
                .addInputTextContent(prompt)
                .role(ResponseInputItem.Message.Role.USER)
                .build()));

        ResponseCreateParams.Builder createParamsBuilder = ResponseCreateParams.builder()
                .model(ChatModel.of("gpt-6-luna"))
                .maxOutputTokens(2048)
                .addTool(GetWeather.class)
                .input(ResponseCreateParams.Input.ofResponse(inputs));

        client.responses().create(createParamsBuilder.build()).output().forEach(item -> {
            if (item.isFunctionCall()) {
                ResponseFunctionToolCall functionCall = item.asFunctionCall();
                System.out.printf("\tTool requested: %s(%s)%n", functionCall.name(), functionCall.arguments());

                inputs.add(ResponseInputItem.ofFunctionCall(functionCall));
                inputs.add(ResponseInputItem.ofFunctionCallOutput(ResponseInputItem.FunctionCallOutput
                        .builder()
                        .callId(functionCall.callId())
                        .outputAsJson(callFunction(functionCall))
                        .build()));
            }
        });

        createParamsBuilder.input(ResponseCreateParams.Input.ofResponse(inputs));

        String answer = client.responses().create(createParamsBuilder.build()).output().stream()
                .flatMap(item -> item.message().stream())
                .flatMap(message -> message.content().stream())
                .flatMap(content -> content.outputText().stream())
                .map(outputText -> outputText.text())
                .collect(Collectors.joining());

        System.out.println("Assistant: " + answer);
    }

    private static Map<String, Object> callFunction(ResponseFunctionToolCall function) {
        if (!function.name().equals("GetWeather")) {
            throw new IllegalArgumentException("Unknown function: " + function.name());
        }

        return function.arguments(GetWeather.class).execute();
    }
}
