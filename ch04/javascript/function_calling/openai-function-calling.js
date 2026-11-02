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

function getWeather(location) {
    const weatherDb = {
        'san francisco': {
            location: 'San Francisco',
            temperature_c: 18,
            condition: 'Sunny',
            humidity_percent: 63,
        },
        'new york': {
            location: 'New York',
            temperature_c: 12,
            condition: 'Cloudy',
            humidity_percent: 71,
        },
        london: {
            location: 'London',
            temperature_c: 10,
            condition: 'Light rain',
            humidity_percent: 82,
        },
    };

    const key = location.trim().toLowerCase();
    return weatherDb[key] ?? {
        location,
        temperature_c: 21,
        condition: 'Unknown (demo data)',
        humidity_percent: 50,
    };
}

const TOOLS = [{
    "type": "function",
    "name": "get_weather",
    "description": "Get the current weather in a location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "Location to look up."
            }
        },
        "required": ["location"]
    }
}];

const FUNCTIONS = {
    "get_weather": ({ location }) => getWeather(location)
};

async function queryModel(prompt, model = "gpt-6-luna") {
    let response = await client.responses.create({
        model: model,
        input: prompt,
        tools: TOOLS,
        tool_choice: "required",
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
                "output": JSON.stringify(result),
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

const prompt = "What is the weather in San Francisco?";
console.log("User:", prompt);
const response = await queryModel(prompt);
console.log("Assistant:", response);
