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


STEPS = [
    ("start", ("hi", "hello", "help"), "collect details", "Welcome. What can I help you with today?"),
    ("collect details", ("issue", "problem", "need"), "resolve", "Thanks. I have enough to move to the next step."),
    ("resolve", ("confirm", "confirmed", "yes"), "done", "Great, the journey is complete."),
]


def advance(state: str, message: str) -> tuple[str, str]:
    text = message.lower()
    for current, triggers, next_state, reply in STEPS:
        if current == state and any(word in text for word in triggers):
            return next_state, reply
    return state, "I am waiting for the next step in the journey."


def main() -> None:
    state = "start"
    for sample in ["Hi", "Here is my issue", "Confirmed"]:
        print(f"State: {state}")
        print(f"User: {sample}")
        state, reply = advance(state, sample)
        print(f"Agent: {reply}")
        print()


if __name__ == "__main__":
    main()
