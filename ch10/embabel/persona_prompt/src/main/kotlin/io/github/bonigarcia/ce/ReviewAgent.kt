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
import com.embabel.agent.domain.library.HasContent
import com.embabel.agent.prompt.persona.Persona

// A reusable instruction fragment, contributed to any prompt that needs it
val TechnicalEditor = Persona(
    name = "Technical editor",
    persona = "An editor of software engineering documentation",
    voice = "Direct and concrete",
    objective = "Remove vague claims and keep every sentence checkable",
)

data class Draft(
    val text: String,
)

data class ReviewedDraft(
    val draft: Draft,
    val review: String,
) : HasContent {

    override val content: String
        get() = "DRAFT\n" + draft.text + "\n\nREVIEW\n" + review
}

@Agent(description = "Write a short technical paragraph and review it as an editor")
class ReviewAgent {

    @Action
    fun writeDraft(userInput: UserInput, context: OperationContext): Draft =
        context.ai().withDefaultLlm().createObject(
            "Write one short technical paragraph about: ${userInput.content}"
        )

    @AchievesGoal(description = "A draft has been written and reviewed")
    @Action
    fun review(draft: Draft, context: OperationContext): ReviewedDraft {
        val review = context.ai()
            .withDefaultLlm()
            .withPromptContributor(TechnicalEditor)
            .generateText("Review this paragraph in two sentences: ${draft.text}")

        return ReviewedDraft(draft, review)
    }
}
