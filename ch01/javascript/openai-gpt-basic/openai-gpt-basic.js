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
import { performance } from 'perf_hooks';

const client = new OpenAI(); // OPENAI_API_KEY should be set as an environment variable

async function queryModel(userPrompt, model = "gpt-6-luna", maxTokens = 4096, temperature = 0, reasoning = "none") {
    const params = {
        model: model,
        input: userPrompt,
        max_output_tokens: maxTokens,
        reasoning: { effort: reasoning },
    };

    // Sampling controls such as temperature are accepted only without reasoning
    if (reasoning === "none") {
        params.temperature = temperature;
    }

    const start = performance.now();
    const response = await client.responses.create(params);
    const latency = (performance.now() - start) / 1000;

    // Log some details about the response
    const usage = response.usage;
    console.log(`\tModel: ${response.model}`);
    console.log(`\tLatency: ${latency.toFixed(3)} seconds`);
    console.log(`\tInput tokens: ${usage.input_tokens}`);
    console.log(`\tOutput tokens: ${usage.output_tokens}`);
    console.log(`\tReasoning tokens: ${usage.output_tokens_details.reasoning_tokens}`);
    console.log(`\tTotal tokens: ${usage.total_tokens}`);

    return response.output_text;
}

const userPrompt = "How many tokens are in your context window?";

console.log("=== Without reasoning ===");
console.log("User:", userPrompt);
var response = await queryModel(userPrompt);
console.log("AI:", response);

console.log("=== With reasoning ===");
console.log("User:", userPrompt);
response = await queryModel(userPrompt, "gpt-6-luna", 4096, 0, "medium");
console.log("AI:", response);