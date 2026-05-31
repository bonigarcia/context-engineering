package io.github.bonigarcia.ce;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class SpringAiToolUseApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringAiToolUseApplication.class, args);
    }

    @Bean
    CommandLineRunner run(ChatClient.Builder chatClientBuilder) {
        ChatClient chatClient = chatClientBuilder.build();

        return args -> {
            String response = chatClient.prompt()
                    .tools(new MathTools())
                    .user("What is 12 plus 30? Reply with just the number.")
                    .call()
                    .content();

            System.out.println(response);
        };
    }

    static class MathTools {

        @Tool(description = "Add two whole numbers and return the sum")
        int add(
                @ToolParam(description = "first whole number") int a,
                @ToolParam(description = "second whole number") int b) {
            return a + b;
        }
    }
}
