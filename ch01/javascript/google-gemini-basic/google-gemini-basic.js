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
import { GoogleGenerativeAI } from "@google/generative-ai";
import { performance } from 'perf_hooks';

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY); // GOOGLE_API_KEY should be set as an environment variable

async function queryModel(userPrompt, modelName = "gemini-2.5-flash", temperature = 0, maxTokens = 1024, thinkingBudget = 512) {
    const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
    const model = genAI.getGenerativeModel({
        model: modelName,
        generationConfig: {
            temperature: temperature,
            maxOutputTokens: maxTokens,
            thinkingConfig: {
                thinkingBudget: thinkingBudget
            }
        }
    });
    const start = performance.now();
    const result = await model.generateContent(userPrompt);
    const response = await result.response;
    const latency = (performance.now() - start) / 1000;

    const usage = response.usageMetadata;
    console.log(`\tLatency: ${latency.toFixed(3)} seconds`);
    console.log(`\tPrompt tokens: ${usage.promptTokenCount}`);
    console.log(`\tOutput tokens: ${usage.candidatesTokenCount}`);
    console.log(`\tThinking tokens: ${usage.thoughtsTokenCount}`);
    console.log(`\tTotal tokens: ${usage.totalTokenCount}`);

    return response.text();
}

const userPrompt = "How many tokens is your context window?";

console.log("=== Basic model  ===");
console.log("User:", userPrompt);
var response = await queryModel(userPrompt);
console.log("Gemini-2.5:", response);

console.log("=== Advanced model  ===");
console.log("User:", userPrompt);
response = await queryModel(userPrompt, "gemini-3.1-flash-lite-preview");
console.log("Gemini-3.1:", response);