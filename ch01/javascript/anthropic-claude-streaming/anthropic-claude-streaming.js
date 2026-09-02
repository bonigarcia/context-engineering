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

const client = new Anthropic(); // ANTHROPIC_API_KEY should be set as an environment variable

async function queryModel(userPrompt, model = "claude-haiku-4-5", maxTokens = 2048) {
    const start = performance.now();
    let firstToken = null;
    let answer = '';

    const stream = client.messages.stream({
        model: model,
        max_tokens: maxTokens,
        messages: [
            { role: "user", content: userPrompt }
        ],
    });

    stream.on('text', (textDelta) => {
        if (firstToken === null) {
            firstToken = (performance.now() - start) / 1000;
        }
        process.stdout.write(textDelta);
        answer += textDelta;
    });

    const message = await stream.finalMessage();
    const latency = (performance.now() - start) / 1000;
    console.log();

    const usage = message.usage;
    const ttft = firstToken === null ? latency : firstToken;
    console.log(`\tModel: ${message.model}`);
    console.log(`\tTime to first token: ${ttft.toFixed(3)} seconds`);
    console.log(`\tLatency: ${latency.toFixed(3)} seconds`);
    console.log(`\tInput tokens: ${usage.input_tokens}`);
    console.log(`\tOutput tokens: ${usage.output_tokens}`);
    console.log(`\tTotal tokens: ${usage.input_tokens + usage.output_tokens}`);

    return answer.trim();
}

const userPrompt = 'How many tokens are in your context window?';

console.log('User:', userPrompt);
process.stdout.write('Claude: ');
await queryModel(userPrompt);
