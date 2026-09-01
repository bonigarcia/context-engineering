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
package io.github.bonigarcia.ce

import com.embabel.agent.api.invocation.AgentInvocation
import com.embabel.agent.core.AgentPlatform
import com.embabel.agent.domain.io.UserInput
import org.springframework.boot.CommandLineRunner
import org.springframework.boot.SpringApplication
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.context.annotation.Bean
import kotlin.system.exitProcess

@SpringBootApplication
class PersonaPromptApplication {

    @Bean
    fun run(agentPlatform: AgentPlatform) = CommandLineRunner {
        val reviewed = AgentInvocation.builder(agentPlatform)
            .build(ReviewedDraft::class.java)
            .invoke(UserInput("why context windows are a budget and not a container"))

        println(reviewed.content)
    }
}

fun main(args: Array<String>) {
    // Embabel starts a web context, so close it once the runner has finished
    exitProcess(SpringApplication.exit(runApplication<PersonaPromptApplication>(*args)))
}
