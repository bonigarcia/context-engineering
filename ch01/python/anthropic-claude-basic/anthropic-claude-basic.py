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


def query_model(prompt: str, model: str = "claude-sonnet-4-20250514", temperature: float = 0) -> str:
    """Send a text prompt to an Anthropic model and return the text response."""

    client = Anthropic()  # ANTHROPIC_API_KEY should be set as an environment variable

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        temperature=temperature,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text


if __name__ == "__main__":
    prompt = "How many tokens is your context window?"
    response = query_model(prompt)
    print("User:", prompt)
    print("AI:", response)
