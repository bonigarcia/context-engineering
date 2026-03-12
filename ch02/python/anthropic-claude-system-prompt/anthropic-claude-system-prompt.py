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


def query_model(instructions: str | None, prompt: str, model: str = "claude-sonnet-4-20250514", temperature: float = 0) -> str:
    """Send a text prompt to an Anthropic model and return the text response."""

    client = Anthropic()  # ANTHROPIC_API_KEY should be set as an environment variable

    params = {
        "model": model,
        "max_tokens": 1024,
        "temperature": temperature,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    if instructions:
        params["system"] = instructions

    message = client.messages.create(**params)
    return message.content[0].text


if __name__ == "__main__":
    instructions = """
    You are a strict grammar teacher.
    Always respond in one sentence and correct any mistakes.
    """
    prompt = "Explain me what is context engineering in simple words"
    model = "claude-sonnet-4-20250514"
    temperature = 0

    print("=== With system instructions ===")
    response = query_model(instructions, prompt, model, temperature)
    print("User query:", prompt)
    print("Response:", response)

    print("\n=== With only user prompt ===")
    response = query_model(None, prompt, model, temperature)
    print("User query:", prompt)
    print("Response:", response)
