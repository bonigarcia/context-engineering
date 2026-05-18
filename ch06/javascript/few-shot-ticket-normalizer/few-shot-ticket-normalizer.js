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

function buildMessages(report) {
    return [
        {
            role: 'system',
            content: 'You normalize bug reports into compact support tickets. Return only valid JSON with the keys title, category, priority, summary, and next_step.',
        },
        {
            role: 'user',
            content: 'Bug report:\nThe mobile app crashes when I try to upload a 20 MB PDF. It worked yesterday.',
        },
        {
            role: 'assistant',
            content: JSON.stringify({
                title: 'Crash when uploading large PDF',
                category: 'file_upload',
                priority: 'high',
                summary: 'The mobile app crashes during PDF upload when the file is around 20 MB.',
                next_step: 'Investigate upload limits and crash logs for the mobile client.',
            }, null, 2),
        },
        {
            role: 'user',
            content: 'Bug report:\nSearch results on the dashboard take a long time to load, especially in the morning.',
        },
        {
            role: 'assistant',
            content: JSON.stringify({
                title: 'Slow dashboard search',
                category: 'performance',
                priority: 'medium',
                summary: 'Dashboard search becomes slow, with the issue being most visible during morning usage.',
                next_step: 'Check query latency, indexing, and peak-time load on the search service.',
            }, null, 2),
        },
        {
            role: 'user',
            content: `Bug report:\n${report}\n\nReturn only JSON.`,
        },
    ];
}

async function normalizeReport(model, report) {
    const response = await client.chat.completions.create({
        model,
        messages: buildMessages(report),
        temperature: 0,
        response_format: { type: 'json_object' },
    });
    const content = response.choices[0].message.content ?? '{}';
    return JSON.parse(content);
}

const report = `
The app logs me out whenever I close the browser tab.
I already checked the password manager, and I have to sign in every time.
`.trim();

if (!process.env.OPENAI_API_KEY) {
    throw new Error('OPENAI_API_KEY is not set');
}

const ticket = await normalizeReport(DEFAULT_MODEL, report);

console.log('=== Few-shot ticket normalizer ===');
console.log('Bug report:');
console.log(report);
console.log('\nNormalized ticket:');
console.log(JSON.stringify(ticket, null, 2));
