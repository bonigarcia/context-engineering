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

import com.embabel.agent.api.annotation.AchievesGoal
import com.embabel.agent.api.annotation.Action
import com.embabel.agent.api.annotation.Agent
import com.embabel.agent.api.common.OperationContext
import com.embabel.agent.api.common.createObject
import com.embabel.agent.domain.io.UserInput

data class Question(
    val text: String,
    val topic: String,
)

data class Answer(
    val text: String,
    val source: String,
)

data class DeliveredAnswer(
    val content: String,
)

@Agent(description = "Answer a customer question from the knowledge base or from the model")
class AnswerAgent {

    private val knownAnswers = mapOf(
        "vpn" to "Open the local client and choose the office profile."
    )

    @Action
    fun parseQuestion(userInput: UserInput, context: OperationContext): Question =
        context.ai().withDefaultLlm().createObject(
            "Extract the question and a one-word topic from this message: ${userInput.content}"
        )

    // The cheapest route the planner can take, and it may fail
    @Action(cost = 0.0)
    fun lookUpAnswer(question: Question): Answer? =
        knownAnswers[question.topic.lowercase()]?.let { Answer(it, "knowledge base") }

    // The fallback route, chosen only when the lookup returns nothing
    @Action(cost = 10.0)
    fun generateAnswer(question: Question, context: OperationContext): Answer =
        context.ai().withDefaultLlm().createObject(
            "Answer this support question in one sentence: ${question.text}"
        )

    @AchievesGoal(description = "An answer has been delivered to the customer")
    @Action
    fun deliver(answer: Answer): DeliveredAnswer =
        DeliveredAnswer("${answer.text} (from ${answer.source})")
}
