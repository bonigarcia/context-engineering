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

import java.util.List;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.evaluation.FactCheckingEvaluator;
import org.springframework.ai.chat.evaluation.RelevancyEvaluator;
import org.springframework.ai.document.Document;
import org.springframework.ai.evaluation.EvaluationRequest;
import org.springframework.ai.evaluation.EvaluationResponse;
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
        FactCheckingEvaluator factCheck = FactCheckingEvaluator.builder(builder)
                .build();
        RelevancyEvaluator relevancy = RelevancyEvaluator.builder().build();

        return args -> {
            String question = "How do I reset my password?";
            String context = "Password reset: use the self-service portal, then sign in again.";
            String answer = "Use the self-service portal.";
            List<Document> docs = List.of(new Document(context));

            EvaluationRequest request = new EvaluationRequest(question,
                    docs, answer);

            EvaluationResponse factResult = factCheck.evaluate(request);
            EvaluationResponse relResult = relevancy.evaluate(request);

            System.out.println("Question: " + question);
            System.out.println("Answer: " + answer);
            System.out.println("Context: " + context);
            System.out.println("---");
            System.out.println("FactCheck:  "
                    + (factResult.isPass() ? "PASS" : "FAIL")
                    + " — " + factResult.getFeedback());
            System.out.println("Relevancy:  "
                    + (relResult.isPass() ? "PASS" : "FAIL")
                    + " — " + relResult.getFeedback());
        };
    }
}