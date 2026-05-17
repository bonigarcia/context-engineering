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

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;
import com.openai.models.chat.completions.ChatCompletionCreateParams.Builder;

public class WorkflowStateHandoff {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    static class WorkflowState {
        String objective = "";
        String status = "idle";
        int currentStep = 0;
        List<String> plan = new ArrayList<>();
        List<String> blockers = new ArrayList<>();
        String plannerNotes = "";
        String executorNotes = "";
        int turnCount = 0;
        List<String> handoffLog = new ArrayList<>();

        String render() {
            return String.join("\n", List.of(
                    "- objective: " + (objective.isBlank() ? "(unset)" : objective),
                    "- status: " + status,
                    "- current_step: " + currentStep,
                    "- plan: " + (plan.isEmpty() ? "(none)" : plan),
                    "- blockers: " + (blockers.isEmpty() ? "(none)" : blockers),
                    "- planner_notes: " + (plannerNotes.isBlank() ? "(none)" : plannerNotes),
                    "- executor_notes: " + (executorNotes.isBlank() ? "(none)" : executorNotes),
                    "- turn_count: " + turnCount,
                    "- handoff_log: " + (handoffLog.isEmpty() ? "(none)" : handoffLog.subList(Math.max(0, handoffLog.size() - 4), handoffLog.size()))));
        }
    }

    record TranscriptItem(String role, String content) {
    }

    private final OpenAIClient client;
    private final ChatModel model;
    private final Path statePath;
    private final WorkflowState state = new WorkflowState();

    public WorkflowStateHandoff(ChatModel model, Path statePath) {
        this.client = OpenAIOkHttpClient.fromEnv();
        this.model = model;
        this.statePath = statePath;
    }

    WorkflowState loadState() {
        if (!Files.exists(statePath)) {
            return new WorkflowState();
        }
        try {
            JsonNode data = MAPPER.readTree(statePath.toFile());
            WorkflowState loaded = new WorkflowState();
            loaded.objective = data.path("objective").asText("");
            loaded.status = data.path("status").asText("idle");
            loaded.currentStep = data.path("currentStep").asInt(0);
            loaded.plan = readStringList(data.path("plan"));
            loaded.blockers = readStringList(data.path("blockers"));
            loaded.plannerNotes = data.path("plannerNotes").asText("");
            loaded.executorNotes = data.path("executorNotes").asText("");
            loaded.turnCount = data.path("turnCount").asInt(0);
            loaded.handoffLog = readStringList(data.path("handoffLog"));
            return loaded;
        } catch (IOException e) {
            return new WorkflowState();
        }
    }

    void saveState(WorkflowState current) throws IOException {
        MAPPER.writerWithDefaultPrettyPrinter().writeValue(statePath.toFile(), current);
    }

    static List<String> readStringList(JsonNode node) {
        List<String> values = new ArrayList<>();
        if (node.isArray()) {
            node.forEach(item -> {
                String text = item.asText("").trim();
                if (!text.isBlank()) {
                    values.add(text);
                }
            });
        }
        return values;
    }

    static List<String> ensureList(Object value) {
        if (value instanceof List<?> list) {
            List<String> values = new ArrayList<>();
            for (Object item : list) {
                String text = String.valueOf(item).trim();
                if (!text.isBlank()) {
                    values.add(text);
                }
            }
            return values;
        }
        if (value instanceof String str && !str.isBlank()) {
            return List.of(str.trim());
        }
        return List.of();
    }

    String renderState(WorkflowState current) {
        return current.render();
    }

    String buildPlannerPrompt(WorkflowState current, String userRequest) {
        return "Shared workflow state:\n" + renderState(current) + "\n\nUser request:\n" + userRequest
                + "\n\nReturn JSON with these keys:\n- objective: concise statement of the current goal\n- plan: ordered list of 3 to 5 short steps\n- handoff_note: short note for the executor agent\n- risks: list of likely blockers or assumptions";
    }

    String buildExecutorPrompt(WorkflowState current) {
        return "You are the executor agent in a two-agent workflow.\n\nRead the shared workflow state carefully and continue from the current plan.\n\nShared workflow state:\n"
                + renderState(current)
                + "\n\nReturn JSON with these keys:\n- status: one of idle, planned, in_progress, blocked, or complete\n- completed_step: short description of the step just completed\n- blockers: list of unresolved blockers\n- next_step: short description of the next step to take";
    }

    String sanitizeJson(String raw) {
        String trimmed = raw.trim();
        if (trimmed.startsWith("```")) {
            trimmed = trimmed.replaceFirst("^```(?:json)?\\s*", "");
            trimmed = trimmed.replaceFirst("\\s*```$", "");
        }
        return trimmed;
    }

    JsonNode requestJson(String instructions, String prompt) throws JsonProcessingException {
        Builder builder = ChatCompletionCreateParams.builder().model(model);
        builder.addSystemMessage(instructions);
        builder.addUserMessage(prompt);
        ChatCompletion completion = client.chat().completions().create(builder.build());
        String raw = completion.choices().get(0).message().content().orElse("{}");
        try {
            return MAPPER.readTree(sanitizeJson(raw));
        } catch (JsonProcessingException e) {
            ObjectNode fallback = MAPPER.createObjectNode();
            fallback.put("raw", raw);
            return fallback;
        }
    }

    void applyPlannerResult(WorkflowState current, JsonNode payload) {
        String objective = payload.path("objective").asText("").trim();
        if (!objective.isBlank()) {
            current.objective = objective;
        }
        List<String> plan = readStringList(payload.path("plan"));
        if (!plan.isEmpty()) {
            current.plan = plan;
            current.currentStep = 0;
        }
        String handoffNote = payload.path("handoff_note").asText("").trim();
        if (!handoffNote.isBlank()) {
            current.plannerNotes = handoffNote;
        }
        List<String> risks = readStringList(payload.path("risks"));
        if (!risks.isEmpty()) {
            current.blockers = risks;
        }
        current.status = "planned";
    }

    void applyExecutorResult(WorkflowState current, JsonNode payload) {
        String status = payload.path("status").asText("in_progress").trim();
        current.status = status.isBlank() ? "in_progress" : status;

        String completedStep = payload.path("completed_step").asText("").trim();
        if (!completedStep.isBlank()) {
            current.executorNotes = completedStep;
            current.handoffLog.add("executor: " + completedStep);
        }

        List<String> blockers = readStringList(payload.path("blockers"));
        if (!blockers.isEmpty()) {
            LinkedHashSet<String> merged = new LinkedHashSet<>(current.blockers);
            merged.addAll(blockers);
            current.blockers = new ArrayList<>(merged);
        }

        if (!current.plan.isEmpty() && current.currentStep < current.plan.size()) {
            current.currentStep += 1;
        }

        String nextStep = payload.path("next_step").asText("").trim();
        if (!nextStep.isBlank()) {
            current.handoffLog.add("next: " + nextStep);
        }
    }

    void run() throws IOException {
        if (System.getenv("OPENAI_API_KEY") == null || System.getenv("OPENAI_API_KEY").isBlank()) {
            System.out.println("OPENAI_API_KEY is not set. Put it in your environment or a .env file.");
            System.exit(2);
        }

        WorkflowState loaded = loadState();
        state.objective = loaded.objective;
        state.status = loaded.status;
        state.currentStep = loaded.currentStep;
        state.plan = loaded.plan;
        state.blockers = loaded.blockers;
        state.plannerNotes = loaded.plannerNotes;
        state.executorNotes = loaded.executorNotes;
        state.turnCount = loaded.turnCount;
        state.handoffLog = loaded.handoffLog;

        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        System.out.println("[Workflow state demo] model=" + model + " state_file=" + statePath.toAbsolutePath());
        System.out.println("Type /help for commands.\n");

        while (true) {
            System.out.print("you> ");
            String userText = reader.readLine();
            if (userText == null) {
                System.out.println();
                return;
            }
            userText = userText.trim();
            if (userText.isBlank()) {
                continue;
            }

            if (userText.startsWith("/")) {
                String cmd = userText.toLowerCase().trim();
                switch (cmd) {
                case "/help" -> System.out.println(
                        "Commands:\n  /help    show commands\n  /state   show the shared workflow state\n  /reset   clear the workflow state file\n  /exit    quit\n");
                case "/state" -> System.out.println("Shared workflow state\n" + state.render() + "\n");
                case "/reset" -> {
                    state.objective = "";
                    state.status = "idle";
                    state.currentStep = 0;
                    state.plan.clear();
                    state.blockers.clear();
                    state.plannerNotes = "";
                    state.executorNotes = "";
                    state.turnCount = 0;
                    state.handoffLog.clear();
                    saveState(state);
                    System.out.println("Cleared workflow state.\n");
                }
                case "/exit" -> {
                    System.out.println("Goodbye.");
                    return;
                }
                default -> System.out.println("Unknown command. Type /help.\n");
                }
                continue;
            }

            state.turnCount += 1;
            if (state.objective.isBlank()) {
                state.objective = userText.trim();
            }

            JsonNode plannerPayload = requestJson(
                    "You are the planning agent. Produce concise, structured workflow state.",
                    buildPlannerPrompt(state, userText));
            applyPlannerResult(state, plannerPayload);

            JsonNode executorPayload = requestJson(
                    "You are the execution agent. Advance the shared workflow state.",
                    buildExecutorPrompt(state));
            applyExecutorResult(state, executorPayload);

            saveState(state);

            System.out.println("Planner output");
            System.out.println(MAPPER.writerWithDefaultPrettyPrinter().writeValueAsString(plannerPayload));
            System.out.println("Executor output");
            System.out.println(MAPPER.writerWithDefaultPrettyPrinter().writeValueAsString(executorPayload));
            System.out.println("Shared state");
            System.out.println(state.render());
            System.out.println();
        }
    }

    public static void main(String[] args) throws Exception {
        Path statePath = Path.of(System.getenv().getOrDefault("STATE_FILE", ".workflow_state_handoff.json"))
                .toAbsolutePath();
        new WorkflowStateHandoff(ChatModel.GPT_5, statePath).run();
    }
}
