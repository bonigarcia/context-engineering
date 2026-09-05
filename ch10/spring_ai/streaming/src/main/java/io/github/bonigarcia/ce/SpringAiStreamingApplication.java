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

import reactor.core.Disposable;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class SpringAiStreamingApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringAiStreamingApplication.class, args);
    }

    @Bean
    CommandLineRunner run(ChatClient.Builder builder) {
        ChatClient chatClient = builder.build();

        return args -> {
            String prompt = "Tell me a short joke about programming.";
            System.out.println("User: " + prompt);
            System.out.print("Model: ");

            Disposable subscription = chatClient.prompt()
                    .user(prompt)
                    .stream()
                    .content()
                    .subscribe(System.out::print,
                            error -> System.err.println("Error: " + error),
                            () -> System.out.println());

            Thread.sleep(10000);
            subscription.dispose();
        };
    }
}