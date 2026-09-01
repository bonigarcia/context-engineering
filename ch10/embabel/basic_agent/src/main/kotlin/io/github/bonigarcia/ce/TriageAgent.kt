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

data class Ticket(
    val category: String,
    val urgency: String,
)

data class Reply(
    val text: String,
)

@Agent(description = "Triage a support request and draft a reply for the customer")
class TriageAgent {

    // The parameter type is the precondition, the return type is the postcondition
    @Action
    fun classify(userInput: UserInput, context: OperationContext): Ticket =
        context.ai().withDefaultLlm().createObject(
            "Classify this support request into a category and an urgency: ${userInput.content}"
        )

    @AchievesGoal(description = "A reply has been drafted for the support request")
    @Action
    fun draftReply(ticket: Ticket, context: OperationContext): Reply =
        context.ai().withDefaultLlm().createObject(
            "Draft a two-sentence reply for a ${ticket.urgency} ${ticket.category} request"
        )
}
