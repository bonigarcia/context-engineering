"""
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
"""
from google import genai
from google.genai import types


def query_model(prompt: str, model: str = "gemini-2.0-flash", temperature: float = 0) -> str:
    """Send a text prompt to a Google Gemini model and return the text response."""

    client = genai.Client()  # GOOGLE_API_KEY should be set as an environment variable
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
        ),
    )
    return response.text


if __name__ == "__main__":
    prompt = "How many tokens is your context window?"
    response = query_model(prompt)
    print("User:", prompt)
    print("AI:", response)
