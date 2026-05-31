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

from __future__ import annotations


GUIDELINES = [
    (("hello", "hi", "greet"), "offer a refreshing drink and ask how you can help"),
    (("financing", "loan", "payment"), "explain financing options and next steps"),
    (("trade in", "trade-in", "trade"), "ask for the current vehicle details and mileage"),
]


def route(message: str) -> str:
    text = message.lower()
    for keywords, action in GUIDELINES:
        if any(keyword in text for keyword in keywords):
            return action
    return "fall back to a general response"


def main() -> None:
    samples = [
        "Hello there, I just arrived.",
        "Do you have financing available?",
        "I want to trade in my old car.",
    ]
    for sample in samples:
        print(f"User: {sample}")
        print(f"Routed guideline: {route(sample)}")
        print()


if __name__ == "__main__":
    main()
