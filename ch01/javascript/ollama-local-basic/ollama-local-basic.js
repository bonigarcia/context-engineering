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
import { performance } from 'node:perf_hooks';

const ollamaHost = process.env.OLLAMA_HOST || 'http://localhost:11434';
const ollamaModel = process.env.OLLAMA_MODEL || 'gemma3:4b';

async function queryModel(userPrompt, model = ollamaModel, temperature = 0) {
    const payload = {
        model: model,
        prompt: userPrompt,
        stream: false,
        options: {
            temperature: temperature,
        },
    };

    const start = performance.now();
    const response = await fetch(`${ollamaHost}/api/generate`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    });
    const latency = (performance.now() - start) / 1000;

    if (!response.ok) {
        throw new Error(`Ollama request failed: ${await response.text()}`);
    }

    const result = await response.json();
    const inputTokens = result.prompt_eval_count || 0;
    const outputTokens = result.eval_count || 0;

    console.log(`\tModel: ${result.model || model}`);
    console.log(`\tLatency: ${latency.toFixed(3)} seconds`);
    console.log(`\tInput tokens: ${inputTokens}`);
    console.log(`\tOutput tokens: ${outputTokens}`);
    console.log(`\tTotal tokens: ${inputTokens + outputTokens}`);

    return result.response.trim();
}

const userPrompt = 'How many tokens is your context window?';

console.log('User:', userPrompt);
const response = await queryModel(userPrompt);
console.log('Local LLM:', response);
