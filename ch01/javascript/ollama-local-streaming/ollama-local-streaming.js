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
        stream: true,
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

    if (!response.ok) {
        throw new Error(`Ollama request failed: ${await response.text()}`);
    }

    const decoder = new TextDecoder();
    let firstToken = null;
    let buffer = '';
    let answer = '';
    let stats = {};

    for await (const bytes of response.body) {
        buffer += decoder.decode(bytes, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop();
        for (const line of lines) {
            if (!line.trim()) {
                continue;
            }
            const chunk = JSON.parse(line);
            const text = chunk.response || '';
            if (text && firstToken === null) {
                firstToken = (performance.now() - start) / 1000;
            }
            process.stdout.write(text);
            answer += text;
            if (chunk.done) {
                stats = chunk;
            }
        }
    }
    const latency = (performance.now() - start) / 1000;
    console.log();

    const inputTokens = stats.prompt_eval_count || 0;
    const outputTokens = stats.eval_count || 0;
    const ttft = firstToken === null ? latency : firstToken;

    console.log(`\tModel: ${stats.model || model}`);
    console.log(`\tTime to first token: ${ttft.toFixed(3)} seconds`);
    console.log(`\tLatency: ${latency.toFixed(3)} seconds`);
    console.log(`\tInput tokens: ${inputTokens}`);
    console.log(`\tOutput tokens: ${outputTokens}`);
    console.log(`\tTotal tokens: ${inputTokens + outputTokens}`);

    return answer.trim();
}

const userPrompt = 'How many tokens are in your context window?';

console.log('User:', userPrompt);
process.stdout.write('Local LLM: ');
await queryModel(userPrompt);
