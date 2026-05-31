package io.github.bonigarcia.ce;

import java.util.List;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.vectorstore.QuestionAnswerAdvisor;
import org.springframework.ai.document.Document;
import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.vectorstore.SimpleVectorStore;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class SpringAiRagRetrievalApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringAiRagRetrievalApplication.class, args);
    }

    @Bean
    VectorStore vectorStore(EmbeddingModel embeddingModel) {
        return SimpleVectorStore.builder(embeddingModel).build();
    }

    @Bean
    CommandLineRunner run(ChatClient.Builder chatClientBuilder, VectorStore vectorStore) {
        vectorStore.add(List.of(
                new Document("Reset password: use the self-service portal, then sign in again."),
                new Document("VPN access: open the local client and choose the office profile."),
                new Document("Invoice copy: download the latest invoice from the billing page.")));

        ChatClient chatClient = chatClientBuilder.build();

        return args -> {
            String answer = chatClient.prompt()
                    .advisors(QuestionAnswerAdvisor.builder(vectorStore).build())
                    .user("How do I reset my password?")
                    .call()
                    .content();

            System.out.println(answer);
        };
    }
}
