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

function getCurrentTime(args) {
    let { format } = args || {};
    const now = new Date();
    if (!format) {
        return now.toLocaleString('en-GB', { hour12: false }).replace(',', '');
    }
    // Simple mock of strftime for common patterns used in this repo
    return now.toLocaleString('en-GB', { hour12: false }).replace(',', '');
}

const TOOLS = [{
    "type": "function",
    "name": "get_current_time",
    "description": "Get the current system time.",
    "parameters": {
        "type": "object",
        "properties": {
            "format": {
                "type": "string",
                "description": "Python strftime format string (optional)."
            }
        },
        "required": []
    }
}];

const FUNCTIONS = {
    "get_current_time": getCurrentTime
};

async function queryModel(prompt, model = "gpt-4o-mini") {
    let response = await client.responses.create({
        model: model,
        input: prompt,
        tools: TOOLS,
    });

    while (true) {
        const calls = response.output.filter(item => item.type === "function_call");

        if (calls.length === 0) {
            return response.output_text;
        }

        const outputs = [];
        for (const call of calls) {
            const toolName = call.name;
            const args = JSON.parse(call.arguments || "{}");
            console.log(`\tTool requested: ${toolName}(${JSON.stringify(args)})`);

            const result = FUNCTIONS[toolName](args);

            outputs.push({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": result,
            });
        }

        response = await client.responses.create({
            model: model,
            previous_response_id: response.id,
            input: outputs,
            tools: TOOLS,
        });
    }
}

const prompt = "What time is it right now?";
console.log("User:", prompt);
const response = await queryModel(prompt);
console.log("Assistant:", response);
