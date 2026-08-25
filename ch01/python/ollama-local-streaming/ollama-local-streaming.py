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
import json
import os
import time

import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")


def query_model(prompt: str,
                model: str = OLLAMA_MODEL,
                temperature: float = 0) -> str:
    """Stream the response of a local LLM running through Ollama."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": temperature,
        },
    }

    start = time.perf_counter()
    first_token = None
    chunks = []
    stats = {}
    with requests.post(f"{OLLAMA_HOST}/api/generate",
                       json=payload,
                       stream=True,
                       timeout=120) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            chunk = json.loads(line)
            text = chunk.get("response", "")
            if text and first_token is None:
                first_token = time.perf_counter() - start
            print(text, end="", flush=True)
            chunks.append(text)
            if chunk.get("done"):
                stats = chunk
    latency = time.perf_counter() - start
    print()

    input_tokens = stats.get("prompt_eval_count", 0)
    output_tokens = stats.get("eval_count", 0)
    ttft = first_token if first_token is not None else latency
    print(f"\tModel: {stats.get('model', model)}")
    print(f"\tTime to first token: {ttft:.3f} seconds")
    print(f"\tLatency: {latency:.3f} seconds")
    print(f"\tInput tokens: {input_tokens}")
    print(f"\tOutput tokens: {output_tokens}")
    print(f"\tTotal tokens: {input_tokens + output_tokens}")

    return "".join(chunks).strip()


if __name__ == "__main__":
    prompt = "How many tokens are in your context window?"

    print("User:", prompt)
    print("Local LLM: ", end="", flush=True)
    query_model(prompt)
