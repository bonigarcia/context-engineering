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
