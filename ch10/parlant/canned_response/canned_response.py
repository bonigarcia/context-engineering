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


RESPONSE_TEMPLATES = {
    "shipping delay": "We are sorry for the delay. I am checking the latest status now.",
    "billing issue": "Thanks for flagging this. I will connect you with the billing team.",
    "order status": "I can help with that. Please share your order number.",
}


def choose_response(message: str) -> str:
    text = message.lower()
    for intent, template in RESPONSE_TEMPLATES.items():
        if intent in text:
            return template
    return "Thanks for reaching out. I will help with that."


def main() -> None:
    samples = [
        "There is a shipping delay on my order.",
        "I found a billing issue.",
        "Can you check the order status?",
    ]
    for sample in samples:
        print(f"User: {sample}")
        print(f"Template: {choose_response(sample)}")
        print()


if __name__ == "__main__":
    main()
