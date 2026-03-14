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
import { performance } from 'perf_hooks';

const client = new Anthropic(); //  ANTHROPIC_API_KEY should be set as an environment variable

async function queryModel(userPrompt, model = "claude-3-haiku-20240307", maxTokens = 2048, temperature = 0, thinkingBudget = 0) {
    const params = {
        model: model,
        max_tokens: maxTokens,
        messages: [
            { role: "user", content: userPrompt }
        ]
    };
    if (thinkingBudget > 0) {
        params.thinking = {
            type: "enabled",
            budget_tokens: thinkingBudget
        };
    } else {
        params.temperature = temperature;
    }

    const start = performance.now();
    const response = await client.messages.create(params);
    const latency = (performance.now() - start) / 1000;

    // Log some details about the response
    const usage = response.usage;
    console.log(`\tModel: ${response.model}`);
    console.log(`\tLatency: ${latency.toFixed(3)} seconds`);
    console.log(`\tInput tokens: ${usage.input_tokens}`);
    console.log(`\tOutput tokens: ${usage.output_tokens}`);

    let responseText = "";
    for (const block of response.content) {
        if (block.type === "text") {
            responseText += block.text;
        }
    }
    return responseText;
}

const userPrompt = "How many tokens is your context window?";

console.log("=== Basic model  ===");
console.log("User:", userPrompt);
var response = await queryModel(userPrompt);
console.log("Claude3:", response);

console.log("=== Advanced model  ===");
console.log("User:", userPrompt);
response = await queryModel(userPrompt, "claude-sonnet-4-20250514", 2048, 0, 1024);
console.log("Claude4:", response);