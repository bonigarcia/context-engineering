package io.github.bonigarcia.ce;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class SpringAiBasicAssistantApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringAiBasicAssistantApplication.class, args);
    }

    @Bean
    CommandLineRunner run(ChatModel chatModel) {
        ChatClient chatClient = ChatClient.builder(chatModel).build();

        return args -> {
            String response = chatClient.prompt()
                    .user("Reply with one short sentence about what Spring AI does.")
                    .call()
                    .content();

            System.out.println(response);
        };
    }
}
