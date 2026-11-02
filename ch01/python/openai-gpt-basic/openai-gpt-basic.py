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
from openai import OpenAI
import time

client = OpenAI()  # OPENAI_API_KEY should be set as an environment variable


def query_model(prompt: str,
                model: str = "gpt-6-luna",
                max_tokens: int = 4096,
                temperature: float = 0,
                reasoning: str = "none") -> str:
    """Send a user prompt to an OpenAI model and return the text response."""
    params = {
        "model": model,
        "input": prompt,
        "max_output_tokens": max_tokens,
        "reasoning": {"effort": reasoning},
    }
    # Sampling controls such as temperature are accepted only without reasoning
    if reasoning == "none":
        params["temperature"] = temperature

    start = time.perf_counter()
    response = client.responses.create(**params)
    latency = time.perf_counter() - start

    # Log some details about the response
    usage = response.usage
    print(f"\tModel: {response.model}")
    print(f"\tLatency: {latency:.3f} seconds")
    print(f"\tInput tokens: {usage.input_tokens}")
    print(f"\tOutput tokens: {usage.output_tokens}")
    print(f"\tReasoning tokens: {usage.output_tokens_details.reasoning_tokens}")
    print(f"\tTotal tokens: {usage.total_tokens}")

    return response.output_text


if __name__ == "__main__":
    prompt = "How many tokens are in your context window?"

    print("=== Without reasoning ===")
    print("User:", prompt)
    response = query_model(prompt)
    print("AI:", response)

    print("=== With reasoning ===")
    print("User:", prompt)
    response = query_model(prompt, reasoning="medium")
    print("AI:", response)
