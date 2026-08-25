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
import { GoogleGenAI } from '@google/genai';
import { performance } from 'perf_hooks';

const ai = new GoogleGenAI({}); // GOOGLE_API_KEY should be set as an environment variable

async function queryModel(userPrompt, model = "gemini-2.5-flash", temperature = 0, maxTokens = 1024, thinkingBudget = 512) {
    const start = performance.now();
    let firstToken = null;
    let answer = '';
    let usage = null;

    const stream = await ai.models.generateContentStream({
        model: model,
        contents: userPrompt,
        config: {
            temperature: temperature,
            maxOutputTokens: maxTokens,
            thinkingConfig: {
                thinkingBudget: thinkingBudget,
            },
        },
    });

    for await (const chunk of stream) {
        if (chunk.usageMetadata) {
            usage = chunk.usageMetadata;
        }
        const text = chunk.text || '';
        if (!text) {
            continue;
        }
        if (firstToken === null) {
            firstToken = (performance.now() - start) / 1000;
        }
        process.stdout.write(text);
        answer += text;
    }
    const latency = (performance.now() - start) / 1000;
    console.log();

    const ttft = firstToken === null ? latency : firstToken;
    console.log(`\tTime to first token: ${ttft.toFixed(3)} seconds`);
    console.log(`\tLatency: ${latency.toFixed(3)} seconds`);
    if (usage) {
        console.log(`\tPrompt tokens: ${usage.promptTokenCount}`);
        console.log(`\tOutput tokens: ${usage.candidatesTokenCount}`);
        console.log(`\tThinking tokens: ${usage.thoughtsTokenCount}`);
        console.log(`\tTotal tokens: ${usage.totalTokenCount}`);
    }

    return answer.trim();
}

const userPrompt = 'How many tokens are in your context window?';

console.log('User:', userPrompt);
process.stdout.write('Gemini: ');
await queryModel(userPrompt);
