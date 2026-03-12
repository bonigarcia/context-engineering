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
import OpenAI from 'openai';

async function queryModel(instructions, userPrompt, model = "gpt-4o-mini", temperature = 0) {
    // OPENAI_API_KEY should be set as an environment variable
    const client = new OpenAI();

    const messages = [];
    if (instructions) {
        messages.push({ role: "system", content: instructions });
    }
    messages.push({ role: "user", content: userPrompt });

    const response = await client.chat.completions.create({
        model: model,
        messages: messages,
        temperature: temperature,
    });

    return response.choices[0].message.content;
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
