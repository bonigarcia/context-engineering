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
            int tokensBefore = estimator.estimate(doc.getText());
            List<Document> chunks = splitter.split(doc);
            int tokensAfter = estimator.estimate(
                    chunks.stream().map(Document::getText)
                            .reduce("", (a, b) -> a + " " + b));

            System.out.println("Original text: " + longText);
            System.out.println("---");
            System.out.println(
                    "Tokens before: " + tokensBefore + ", chunks: 1");
            System.out.println(
                    "Tokens after:  " + tokensAfter + ", chunks: "
                            + chunks.size());
            System.out.println("Compression:  "
                    + (tokensBefore - tokensAfter) + " tokens removed");
            for (int i = 0; i < chunks.size(); i++) {
                System.out.println("  Chunk " + (i + 1) + ": "
                        + estimator.estimate(chunks.get(i).getText())
                        + " tokens — " + chunks.get(i).getText());
            }

            ChatClient chatClient = builder
                    .defaultSystem(
                            "You are a helpful assistant. Answer concisely.")
                    .build();

            String answer = chatClient.prompt()
                    .user("Summarize this: " + chunks.get(0).getText())
                    .call().content();
            System.out.println("---");
            System.out.println("Summary of first chunk: " + answer);
        };
    }
}