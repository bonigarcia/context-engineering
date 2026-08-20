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

async function analyzeInquiry(model, message) {
    const response = await client.chat.completions.create({
        model,
        messages: [
            {
                role: 'system',
                content: 'Analyze the customer support inquiry. Return only valid JSON with the following keys: category (one of: billing, technical_bug, feature_request, general_inquiry), urgency (one of: low, medium, high, critical), sentiment (one of: positive, neutral, frustrated, angry), summary (a concise 1-sentence summary of the core issue).',
            },
            {
                role: 'user',
                content: `Customer inquiry:\n${message}\n\nReturn only JSON.`,
            },
        ],
        temperature: 0,
        response_format: { type: 'json_object' },
    });

    const content = response.choices[0].message.content ?? '{}';
    return JSON.parse(content);
}

function resolvePolicy(analysis) {
    const category = analysis.category || 'general_inquiry';
    const urgency = analysis.urgency || 'medium';

    if (category === 'billing' && (urgency === 'high' || urgency === 'critical')) {
        return {
            sla_response_time: '1 hour',
            escalation_team: 'Priority Billing & Finance Ops',
            resolution_guidelines: 'Acknowledge the billing discrepancy, confirm expedited review with Finance Ops for refund processing, and provide a direct case tracking reference.',
        };
    } else if (category === 'technical_bug' && (urgency === 'high' || urgency === 'critical')) {
        return {
            sla_response_time: '2 hours',
            escalation_team: 'Tier-2 Engineering',
            resolution_guidelines: 'Acknowledge the technical disruption, outline immediate diagnostic steps, and route logs to Tier-2 Engineering.',
        };
    } else {
        return {
            sla_response_time: '24 hours',
            escalation_team: 'Standard Support',
            resolution_guidelines: 'Provide helpful guidance addressing the customer question and offer links to documentation.',
        };
    }
}

async function draftReply(model, message, analysis, policy) {
    const contextPrompt = `Customer inquiry:
${message}

Case analysis:
- Category: ${analysis.category}
- Urgency: ${analysis.urgency}
- Customer sentiment: ${analysis.sentiment}
- Core issue: ${analysis.summary}

Resolution policy:
- Target SLA response: ${policy.sla_response_time}
- Assigned team: ${policy.escalation_team}
- Guidelines: ${policy.resolution_guidelines}

Draft a professional, empathetic 3 to 4 sentence customer reply adhering to the resolution policy.`;

    const response = await client.chat.completions.create({
        model,
        messages: [
            {
                role: 'system',
                content: 'You are an enterprise customer support specialist. Write a professional, empathetic reply that strictly follows the provided resolution policy and case analysis. Do not mention JSON keys or internal system labels.',
            },
            {
                role: 'user',
                content: contextPrompt,
            },
        ],
        temperature: 0.2,
    });

    return response.choices[0].message.content ?? '';
}

const message = `
We were double-billed on invoice #INV-9821 for our annual Enterprise tier ($4,800 instead of $2,400).
This is blocking our quarterly accounting close, and we need an immediate refund and an updated invoice.
`.trim();

if (!process.env.OPENAI_API_KEY) {
    throw new Error('OPENAI_API_KEY is not set');
}

const analysis = await analyzeInquiry(DEFAULT_MODEL, message);
const policy = resolvePolicy(analysis);
const reply = await draftReply(DEFAULT_MODEL, message, analysis, policy);

console.log('=== Prompt chaining support reply ===');
console.log('Customer message:');
console.log(message);
console.log('\nStep 1: extracted analysis');
console.log(JSON.stringify(analysis, null, 2));
console.log('\nIntermediate: resolved policy');
console.log(JSON.stringify(policy, null, 2));
console.log('\nStep 2: customer reply');
console.log(reply);
