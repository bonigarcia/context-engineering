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
from anthropic import Anthropic
import time

client = Anthropic()  # ANTHROPIC_API_KEY should be set as an environment variable


def query_model(prompt: str,
                model: str = "claude-3-haiku-20240307",
                max_tokens: int = 2048,
                temperature: float = 0,
                thinking_budget: int = 0, ) -> str:
    """Send a user prompt to an Anthropic model and return the text response."""
    params = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    if thinking_budget > 0:
        params["thinking"] = {
            "type": "enabled",
            "budget_tokens": thinking_budget
        }
    else:
        params["temperature"] = temperature

    start = time.perf_counter()
    response = client.messages.create(**params)
    latency = time.perf_counter() - start

    # Log some details about the response
    usage = response.usage
    print(f"\tModel: {response.model}")
    print(f"\tLatency: {latency:.3f} seconds")
    print(f"\tInput tokens: {usage.input_tokens}")
    print(f"\tOutput tokens: {usage.output_tokens}")

    response_text = ""
    for block in response.content:
        if block.type == "text":
            response_text += block.text
    return response_text


if __name__ == "__main__":
    prompt = "How many tokens is your context window?"

    print("=== Basic model ===")
    print("User:", prompt)
    response = query_model(prompt)
    print("Claude3:", response)

    print("=== Advanced model ===")
    print("User:", prompt)
    response = query_model(prompt, model="claude-sonnet-4-20250514", thinking_budget=1024)
    print("Claude4:", response)
