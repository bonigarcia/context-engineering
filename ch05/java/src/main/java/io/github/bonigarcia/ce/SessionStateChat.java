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
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;
import com.openai.models.chat.completions.ChatCompletionCreateParams.Builder;

public class SessionStateChat {

    record TranscriptItem(String role, String content) {
    }

    static class SessionState {
        String goal = "";
        String stage = "collecting_context";
        String topic = "";
        List<String> constraints = new ArrayList<>();
        List<String> openQuestions = new ArrayList<>();
        int turnCount = 0;
        String lastUserMessage = "";
        String lastAssistantMessage = "";

        String render() {
            return String.join("\n", List.of(
                    "- goal: " + (goal.isBlank() ? "(unset)" : goal),
                    "- stage: " + stage,
                    "- topic: " + (topic.isBlank() ? "(unset)" : topic),
                    "- turn_count: " + turnCount,
                    "- constraints: " + (constraints.isEmpty() ? "(none)" : String.join(", ", constraints)),
                    "- open_questions: " + (openQuestions.isEmpty() ? "(none)" : String.join(", ", openQuestions)),
                    "- last_user_message: " + (lastUserMessage.isBlank() ? "(unset)" : lastUserMessage),
                    "- last_assistant_message: " + (lastAssistantMessage.isBlank() ? "(unset)" : lastAssistantMessage)));
        }

        void reset() {
            goal = "";
            stage = "collecting_context";
            topic = "";
            constraints.clear();
            openQuestions.clear();
            turnCount = 0;
            lastUserMessage = "";
            lastAssistantMessage = "";
        }
    }

    private final OpenAIClient client;
    private final ChatModel model;
    private final SessionState state = new SessionState();
    private final List<TranscriptItem> transcript = new ArrayList<>();

    public SessionStateChat(ChatModel model) {
        this.model = model;
        this.client = OpenAIOkHttpClient.fromEnv();
    }

    static String extractTopic(String text) {
        Matcher matcher = Pattern.compile("[A-Za-z][A-Za-z0-9_-]+").matcher(text);
        return matcher.find() ? matcher.group().toLowerCase() : "";
    }

    static boolean looksLikeNewGoal(String text) {
        String lower = text.toLowerCase();
        return lower.contains("instead") || lower.contains("switch to")
                || lower.contains("change to") || lower.contains("new task")
                || lower.contains("new goal") || lower.contains("actually");
    }

    void updateState(String userText, String assistantText) {
        state.turnCount += 1;
        state.lastUserMessage = userText;
        state.lastAssistantMessage = assistantText;

        if (state.goal.isBlank() || looksLikeNewGoal(userText)) {
            state.goal = userText.trim();
            state.topic = extractTopic(userText);
            state.constraints.clear();
            state.openQuestions.clear();
        }

        String lower = userText.toLowerCase();
        if (lower.contains("plan") || lower.contains("outline") || lower.contains("roadmap")) {
            state.stage = "planning";
        } else if (lower.contains("review") || lower.contains("check") || lower.contains("verify")) {
            state.stage = "reviewing";
        } else if (lower.contains("done") || lower.contains("finished") || lower.contains("complete")) {
            state.stage = "done";
        } else {
            state.stage = "working";
        }

        if (state.topic.isBlank()) {
            state.topic = extractTopic(userText);
        }

        Matcher constraintMatcher = Pattern.compile(
                "(?:must|should|needs to|do not|don't)\\s+([^.;!?]+)", Pattern.CASE_INSENSITIVE)
                .matcher(userText);
        if (constraintMatcher.find()) {
            String constraint = constraintMatcher.group(0).trim();
            if (!state.constraints.contains(constraint)) {
                state.constraints.add(constraint);
                if (state.constraints.size() > 5) {
                    state.constraints = new ArrayList<>(state.constraints.subList(state.constraints.size() - 5,
                            state.constraints.size()));
                }
            }
        }

        if (userText.contains("?")) {
            String question = userText.trim().replaceAll("\\?$", "");
            if (!question.isBlank() && !state.openQuestions.contains(question)) {
                state.openQuestions.add(question);
                if (state.openQuestions.size() > 5) {
                    state.openQuestions = new ArrayList<>(state.openQuestions.subList(state.openQuestions.size() - 5,
                            state.openQuestions.size()));
                }
            }
        }
    }

    String buildSystemPrompt() {
        return "You are a helpful assistant in a stateful demo.\n\nThe current session state is:\n"
                + state.render()
                + "\n\nUse the state as the current snapshot of the task. Keep answers concise and grounded in the\n"
                + "information already present in the session. If the user changes goals or constraints, adapt to the\n"
                + "new state instead of assuming older context is still correct.";
    }

    String respond(String systemPrompt) {
        Builder builder = ChatCompletionCreateParams.builder().model(model);
        builder.addSystemMessage(systemPrompt);
        for (TranscriptItem item : transcript) {
            if ("user".equals(item.role())) {
                builder.addUserMessage(item.content());
            } else {
                builder.addAssistantMessage(item.content());
            }
        }
        ChatCompletion completion = client.chat().completions().create(builder.build());
        return completion.choices().get(0).message().content().orElse("");
    }

    void run() throws IOException {
        if (System.getenv("OPENAI_API_KEY") == null || System.getenv("OPENAI_API_KEY").isBlank()) {
            System.out.println("OPENAI_API_KEY is not set. Put it in your environment or a .env file.");
            System.exit(2);
        }

        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        System.out.println("[Session state demo] model=" + model);
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
                        "Commands:\n  /help    show commands\n  /state   show the current session state\n  /reset   clear the session state\n  /exit    quit\n");
                case "/state" -> System.out.println("Current session state\n" + state.render() + "\n");
                case "/reset" -> {
                    state.reset();
                    transcript.clear();
                    System.out.println("Cleared session state.\n");
                }
                case "/exit" -> {
                    System.out.println("Goodbye.");
                    return;
                }
                default -> System.out.println("Unknown command. Type /help.\n");
                }
                continue;
            }

            transcript.add(new TranscriptItem("user", userText));
            String assistantText = respond(buildSystemPrompt()).trim();
            transcript.add(new TranscriptItem("assistant", assistantText));
            updateState(userText, assistantText);
            System.out.println(assistantText);
            System.out.println();
        }
    }

    public static void main(String[] args) throws Exception {
        new SessionStateChat(ChatModel.GPT_5).run();
    }
}
