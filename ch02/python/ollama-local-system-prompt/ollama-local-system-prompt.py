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
import os
import time

import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")


def query_model(instructions: str | None,
                prompt: str,
                model: str = OLLAMA_MODEL,
                temperature: float = 0) -> str:
    """Send a system instruction and a user prompt to a local LLM running through Ollama."""
    messages = []
    if instructions:
        messages.append({"role": "system", "content": instructions})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }

    start = time.perf_counter()
    response = requests.post(f"{OLLAMA_HOST}/api/chat",
                             json=payload,
                             timeout=120)
    latency = time.perf_counter() - start
    response.raise_for_status()
    result = response.json()

    input_tokens = result.get("prompt_eval_count", 0)
    output_tokens = result.get("eval_count", 0)
    print(f"\tModel: {result.get('model', model)}")
    print(f"\tLatency: {latency:.3f} seconds")
    print(f"\tInput tokens: {input_tokens}")
    print(f"\tOutput tokens: {output_tokens}")
    print(f"\tTotal tokens: {input_tokens + output_tokens}")

    return result["message"]["content"].strip()


if __name__ == "__main__":
    instructions = """
    You are a strict grammar teacher.
    Always respond in one sentence and correct any mistakes.
    """
    prompt = "Explain me what is context engineering in simple words"
    model = OLLAMA_MODEL
    temperature = 0

    print("=== With system instructions ===")
    response = query_model(instructions, prompt, model, temperature)
    print("User query:", prompt)
    print("Response:", response)

    print("\n=== With only user prompt ===")
    response = query_model(None, prompt, model, temperature)
    print("User query:", prompt)
    print("Response:", response)
