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

async function queryModel(userPrompt, model = "gpt-4o-mini", maxTokens = 1024, temperature = 0, reasoning = "low") {
    const params = {
        model: model,
        input: userPrompt,
        max_output_tokens: maxTokens,
    };

    if (isGpt5OrAbove(model)) {
        params.reasoning = { effort: reasoning };
    } else {
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

function isGpt5OrAbove(model) {
    return /^gpt-[5-9].*/i.test(model);
}

const userPrompt = "How many tokens is your context window?";

console.log("=== Basic model  ===");
console.log("User:", userPrompt);
var response = await queryModel(userPrompt);
console.log("GPT4:", response);

console.log("=== Advanced model  ===");
console.log("User:", userPrompt);
response = await queryModel(userPrompt, "gpt-5", 1024, 0, "medium");
console.log("GPT5:", response);