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

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class SpringAiEvaluationApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringAiEvaluationApplication.class, args);
    }

    @Bean
    CommandLineRunner run(ChatClient.Builder builder) {
        ChatClient judge = builder
                .defaultSystem("You are a strict evaluator. "
                        + "Score the answer on relevance, correctness, and completeness "
                        + "on a scale of 1-10. Provide brief notes.")
                .build();

        return args -> {
            String question = "How do I reset my password?";
            String context = "Password reset: use the self-service portal, then sign in again.";
            String answer = "Use the self-service portal.";

            EvalResult result = judge.prompt()
                    .user("Question: " + question + "\nContext: " + context
                            + "\nAnswer: " + answer
                            + "\n\nReturn a JSON object with fields: "
                            + "relevance (int 1-10), correctness (int 1-10), "
                            + "completeness (int 1-10), notes (string).")
                    .call().entity(EvalResult.class);

            System.out.println("Question: " + question);
            System.out.println("Answer: " + answer);
            System.out.println("Context: " + context);
            System.out.println("---");
            System.out.println("Evaluation:");
            System.out.println("  relevance:    " + result.relevance() + "/10");
            System.out.println("  correctness:  " + result.correctness()
                    + "/10");
            System.out.println("  completeness: " + result.completeness()
                    + "/10");
            System.out.println("  notes: " + result.notes());
        };
    }

    record EvalResult(int relevance, int correctness, int completeness,
            String notes) {
    }
}