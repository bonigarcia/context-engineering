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
                model: str = "claude-haiku-4-5",
                max_tokens: int = 2048) -> str:
    """Stream the response of an Anthropic model."""
    start = time.perf_counter()
    first_token = None
    chunks = []

    with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {"role": "user", "content": prompt}
        ],
    ) as stream:
        for text in stream.text_stream:
            if first_token is None:
                first_token = time.perf_counter() - start
            print(text, end="", flush=True)
            chunks.append(text)
        message = stream.get_final_message()
    latency = time.perf_counter() - start
    print()

    usage = message.usage
    ttft = first_token if first_token is not None else latency
    print(f"\tModel: {message.model}")
    print(f"\tTime to first token: {ttft:.3f} seconds")
    print(f"\tLatency: {latency:.3f} seconds")
    print(f"\tInput tokens: {usage.input_tokens}")
    print(f"\tOutput tokens: {usage.output_tokens}")
    print(f"\tTotal tokens: {usage.input_tokens + usage.output_tokens}")

    return "".join(chunks).strip()


if __name__ == "__main__":
    prompt = "How many tokens are in your context window?"

    print("User:", prompt)
    print("Claude: ", end="", flush=True)
    query_model(prompt)
