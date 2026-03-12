/*
(C) Copyright 2026 Boni Garcia (https://bonigarcia.github.io/)
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
import Anthropic from '@anthropic-ai/sdk';

async function queryModel(instructions, userPrompt, model = "claude-sonnet-4-20250514", temperature = 0) {
    //  ANTHROPIC_API_KEY should be set as an environment variable
    const client = new Anthropic();

    const params = {
        model: model,
        max_tokens: 1024,
        temperature: temperature,
        messages: [
            { role: "user", content: userPrompt }
        ]
    };
    if (instructions) {
        params.system = instructions;
    }

    const message = await client.messages.create(params);

    return message.content[0].text;
}

const instructions = "You are a strict grammar teacher. Always respond in one sentence and correct any mistakes.";
const prompt = "Explain me what is context engineering in simple words";

console.log("=== With system instructions ===");
queryModel(instructions, prompt)
    .then(response => {
        console.log("User:", prompt);
        console.log("AI:", response);

        console.log("\n=== With only user prompt ===");
        return queryModel(null, prompt);
    })
    .then(response => {
        console.log("User:", prompt);
        console.log("AI:", response);
    })
    .catch(error => {
        console.error("Error:", error);
    });
