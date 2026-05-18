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

const client = new OpenAI();
const DEFAULT_MODEL = process.env.MODEL || 'gpt-4o-mini';

async function extractIssue(model, message) {
    const response = await client.chat.completions.create({
        model,
        messages: [
            {
                role: 'system',
                content: 'Extract the key support fields from a customer message. Return only valid JSON with the keys product, issue, sentiment, urgency, and next_action.',
            },
            {
                role: 'user',
                content: 'Customer message:\nThe dashboard keeps logging me out when I switch tabs. I need to sign in again every time.',
            },
            {
                role: 'assistant',
                content: JSON.stringify({
                    product: 'dashboard',
                    issue: 'Session expires or resets when switching tabs',
                    sentiment: 'frustrated',
                    urgency: 'medium',
                    next_action: 'Check session persistence and browser lifecycle handling.',
                }, null, 2),
            },
            {
                role: 'user',
                content: `Customer message:\n${message}\n\nReturn only JSON.`,
            },
        ],
        temperature: 0,
        response_format: { type: 'json_object' },
    });

    const content = response.choices[0].message.content ?? '{}';
    return JSON.parse(content);
}

async function draftReply(model, extracted) {
    const response = await client.chat.completions.create({
        model,
        messages: [
            {
                role: 'system',
                content: 'You are a support agent. Write a concise reply that acknowledges the issue, summarizes the next step, and stays professional and empathetic.',
            },
            {
                role: 'user',
                content: `Use this structured context to draft the reply:\n${JSON.stringify(extracted, null, 2)}\n\nWrite 3 to 4 sentences. Do not mention the JSON fields.`,
            },
        ],
        temperature: 0.2,
    });

    return response.choices[0].message.content ?? '';
}

const message = `
I keep getting signed out of the app whenever I move between dashboard tabs.
It is happening on both Chrome and Edge, and it is slowing down our team.
`.trim();

if (!process.env.OPENAI_API_KEY) {
    throw new Error('OPENAI_API_KEY is not set');
}

const extracted = await extractIssue(DEFAULT_MODEL, message);
const reply = await draftReply(DEFAULT_MODEL, extracted);

console.log('=== Prompt chaining support reply ===');
console.log('Customer message:');
console.log(message);
console.log('\nStep 1: extracted context');
console.log(JSON.stringify(extracted, null, 2));
console.log('\nStep 2: support reply');
console.log(reply);
