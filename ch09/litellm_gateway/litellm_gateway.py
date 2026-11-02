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
from dataclasses import dataclass

try:
    from litellm import completion
except ImportError:
    def completion(model, messages, mock_response):
        return MockResponse(
            choices=[
                MockChoice(message=MockMessage(content=mock_response))
            ]
        )


@dataclass
class MockMessage:
    content: str


@dataclass
class MockChoice:
    message: MockMessage


@dataclass
class MockResponse:
    choices: list[MockChoice]


PRIMARY_MODEL = "openai/gpt-6-luna"
FALLBACK_MODEL = "anthropic/claude-haiku-4-5"


def gateway_completion(model: str, messages: list[dict[str, str]], mock_response: str):
    return completion(model=model, messages=messages, mock_response=mock_response)


def answer_with_gateway(force_primary_failure: bool = False):
    messages = [
        {
            "role": "user",
            "content": "Summarize why an AI gateway is useful.",
        }
    ]

    try:
        if force_primary_failure:
            raise RuntimeError("Simulated primary provider failure")

        response = gateway_completion(
            PRIMARY_MODEL,
            messages,
            mock_response="Primary provider answer.",
        )
        return PRIMARY_MODEL, response.choices[0].message.content
    except Exception:
        response = gateway_completion(
            FALLBACK_MODEL,
            messages,
            mock_response="Fallback provider answer.",
        )
        return FALLBACK_MODEL, response.choices[0].message.content


def main():
    model, answer = answer_with_gateway(force_primary_failure=False)
    print(f"[INFO] Primary path selected: {model}")
    print(f"[INFO] Response: {answer}")

    model, answer = answer_with_gateway(force_primary_failure=True)
    print(f"[INFO] Fallback path selected: {model}")
    print(f"[INFO] Response: {answer}")


if __name__ == "__main__":
    main()
