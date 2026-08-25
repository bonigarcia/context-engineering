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
                thinking_budget: int = 512) -> str:
    """Stream the response of a Google Gemini model."""
    start = time.perf_counter()
    first_token = None
    chunks = []
    usage = None

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            thinking_config=types.ThinkingConfig(
                thinking_budget=thinking_budget
            ),
        ),
    ):
        if chunk.usage_metadata is not None:
            usage = chunk.usage_metadata
        text = chunk.text or ""
        if not text:
            continue
        if first_token is None:
            first_token = time.perf_counter() - start
        print(text, end="", flush=True)
        chunks.append(text)
    latency = time.perf_counter() - start
    print()

    ttft = first_token if first_token is not None else latency
    print(f"\tTime to first token: {ttft:.3f} seconds")
    print(f"\tLatency: {latency:.3f} seconds")
    if usage is not None:
        print(f"\tPrompt tokens: {usage.prompt_token_count}")
        print(f"\tOutput tokens: {usage.candidates_token_count}")
        print(f"\tThinking tokens: {usage.thoughts_token_count}")
        print(f"\tTotal tokens: {usage.total_token_count}")

    return "".join(chunks).strip()


if __name__ == "__main__":
    prompt = "How many tokens are in your context window?"

    print("User:", prompt)
    print("Gemini: ", end="", flush=True)
    query_model(prompt)
