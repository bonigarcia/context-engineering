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
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public final class FunctionCalling {

    private static final String DEFAULT_FORMAT = "yyyy-MM-dd HH:mm:ss";

    private FunctionCalling() {
    }

    @JsonClassDescription("Gets the current system time.")
    static class GetCurrentTime {

        @JsonPropertyDescription("Java date format pattern (optional).")
        public String format;

        public String execute() {
            String pattern = (format == null || format.isBlank()) ? DEFAULT_FORMAT : format;
            return LocalDateTime.now().format(DateTimeFormatter.ofPattern(pattern));
        }
    }

    public static void main(String[] args) {
        OpenAIClient client = OpenAIOkHttpClient.fromEnv();

        String prompt = "What time is it right now?";
        System.out.println("User: " + prompt);

        List<ResponseInputItem> inputs = new ArrayList<>();
        inputs.add(ResponseInputItem.ofMessage(ResponseInputItem.Message.builder()
                .addInputTextContent(prompt)
                .role(ResponseInputItem.Message.Role.USER)
                .build()));

        ResponseCreateParams.Builder createParamsBuilder = ResponseCreateParams.builder()
                .model(ChatModel.GPT_4O_MINI)
                .maxOutputTokens(2048)
                .addTool(GetCurrentTime.class)
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

    private static String callFunction(ResponseFunctionToolCall function) {
        if (!function.name().equals("GetCurrentTime")) {
            throw new IllegalArgumentException("Unknown function: " + function.name());
        }

        return function.arguments(GetCurrentTime.class).execute();
    }
}
