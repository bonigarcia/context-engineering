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

import java.util.Set;

import dev.langchain4j.model.chat.Capability;
import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.model.ollama.OllamaChatModel;
import dev.langchain4j.service.AiServices;
import dev.langchain4j.service.SystemMessage;

public class StructuredOutput {

    record ReleaseSummary(String title, String priority, String nextStep) {
    }

    interface ReleaseAnalyst {

        @SystemMessage("You summarize release readiness checks.")
        ReleaseSummary summarize(String notes);
    }

    public static void main(String[] args) {
        // The JSON schema is derived from the record and sent with the request
        ChatModel chatModel = OllamaChatModel.builder()
                .baseUrl("http://localhost:11434")
                .modelName("llama3.2:1b")
                .supportedCapabilities(Set.of(Capability.RESPONSE_FORMAT_JSON_SCHEMA))
                .build();

        ReleaseAnalyst analyst = AiServices.create(ReleaseAnalyst.class, chatModel);

        ReleaseSummary summary = analyst.summarize(
                "Smoke tests passed. Two flaky integration tests remain. Release window is tomorrow.");

        System.out.println(summary);
    }
}
