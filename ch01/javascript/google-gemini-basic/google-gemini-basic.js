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
import 'dotenv/config';
import { GoogleGenerativeAI } from "@google/generative-ai";

async function queryModel(userPrompt, modelName = "gemini-2.0-flash", temperature = 0) {
    // GOOGLE_API_KEY should be set as an environment variable
    const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
    const model = genAI.getGenerativeModel({ 
        model: modelName,
        generationConfig: {
            temperature: temperature,
        }
    });

    const result = await model.generateContent(userPrompt);
    const response = await result.response;
    return response.text();
}

const userPrompt = "How many tokens is your context window?";
queryModel(userPrompt)
    .then(response => {
        console.log("User:", userPrompt);
        console.log("AI:", response);
    })
    .catch(error => {
        console.error("Error:", error);
    });
