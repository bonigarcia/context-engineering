package io.github.bonigarcia.ce;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class SpringAiStructuredOutputApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringAiStructuredOutputApplication.class, args);
    }

    @Bean
    CommandLineRunner run(ChatClient.Builder chatClientBuilder) {
        ChatClient chatClient = chatClientBuilder.build();

        return args -> {
            ReleaseSummary summary = chatClient.prompt()
                    .user("Return a JSON object with title, priority, and nextStep for a release readiness check.")
                    .call()
                    .entity(ReleaseSummary.class);

            System.out.println(summary);
        };
    }

    record ReleaseSummary(String title, String priority, String nextStep) {}
}
