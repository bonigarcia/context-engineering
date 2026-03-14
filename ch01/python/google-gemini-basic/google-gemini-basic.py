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
import time

client = genai.Client()  # GOOGLE_API_KEY should be set as an environment variable


def query_model(prompt: str,
                model: str = "gemini-2.5-flash",
                temperature: float = 0,
                max_tokens: int = 1024,
                thinking_budget: int = 512,
                ) -> str:
    """Send a user prompt to a Google Gemini model and return the text response."""
    start = time.perf_counter()
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            thinking_config=types.ThinkingConfig(
                thinking_budget=thinking_budget
            )
        ),
    )
    latency = time.perf_counter() - start

    usage = response.usage_metadata
    print(f"\tLatency: {latency:.3f} seconds")
    print(f"\tPrompt tokens: {usage.prompt_token_count}")
    print(f"\tCached prompt tokens: {usage.cached_content_token_count}")
    print(f"\tOutput tokens: {usage.candidates_token_count}")
    print(f"\tThinking tokens: {usage.thoughts_token_count}")
    print(f"\tTotal tokens: {usage.total_token_count}")
    return response.text


if __name__ == "__main__":
    prompt = "How many tokens is your context window?"

    print("=== Basic model  ===")
    print("User:", prompt)
    response = query_model(prompt)
    print("Gemini-2.5:", response)
    print()
    print("=== Advanced model  ===")
    print("User:", prompt)
    response = query_model(prompt, model="gemini-3.1-flash-lite-preview")
    print("Gemini-3.1:", response)
