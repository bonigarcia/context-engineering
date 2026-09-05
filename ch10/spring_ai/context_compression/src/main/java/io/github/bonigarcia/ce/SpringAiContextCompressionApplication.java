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
import org.springframework.ai.document.Document;
import org.springframework.ai.tokenizer.JTokkitTokenCountEstimator;
import org.springframework.ai.tokenizer.TokenCountEstimator;
import org.springframework.ai.transformer.splitter.TokenTextSplitter;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class SpringAiContextCompressionApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringAiContextCompressionApplication.class, args);
    }

    @Bean
    CommandLineRunner run(ChatClient.Builder builder) {
        TokenCountEstimator estimator = new JTokkitTokenCountEstimator();
        TokenTextSplitter splitter = new TokenTextSplitter(100, 0, 5, 5000,
                true, List.of(',', '.', '!', '?'));

        return args -> {
            String longText = """
                    The quarterly report shows revenue growth of 15% across
                    all regions. The EMEA region contributed 45% of total
                    revenue. The APAC region showed the fastest growth at
                    22%. Operating expenses increased by 8% due to new
                    hiring. Net profit margin improved to 18.5%.
                    Cash flow from operations was strong at $12.4M.
                    The board approved a $0.25 dividend increase.
                    Capital expenditures reached $3.2M for infrastructure
                    upgrades. Customer satisfaction scores improved to 92%.
                    Employee headcount grew by 120 new hires in Q3.
                    """;

            Document doc = new Document(longText);
            int totalTokens = estimator.estimate(doc.getText());
            List<Document> chunks = splitter.split(doc);

            System.out.println("Original text (" + totalTokens + " tokens, "
                    + chunks.size() + " chunks):");

            for (int i = 0; i < chunks.size(); i++) {
                int chunkTokens = estimator
                        .estimate(chunks.get(i).getText());
                System.out.println("  Chunk " + (i + 1) + ": " + chunkTokens
                        + " tokens — " + chunks.get(i).getText());
            }
            System.out.println(
                    "  (Total: " + chunks.size() + " chunks of ≤100 tokens)");

            ChatClient chatClient = builder
                    .defaultSystem(
                            "You are a helpful assistant. Answer concisely.")
                    .build();

            String answer = chatClient.prompt()
                    .user("Summarize this: " + chunks.get(0).getText())
                    .call().content();
            System.out.println("\nSummary of first chunk: " + answer);
        };
    }
}