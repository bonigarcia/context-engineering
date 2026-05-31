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


GLOSSARY = {
    "service appointment": "a scheduled visit for maintenance or repair",
    "loaner": "a temporary replacement vehicle",
    "inspection": "a check of vehicle condition and safety",
}


def explain(message: str) -> list[str]:
    text = message.lower()
    matches = []
    for term, definition in GLOSSARY.items():
        if term in text:
            matches.append(f"{term}: {definition}")
    return matches or ["No glossary term matched; keep the interpretation broad."]


def main() -> None:
    sample = "I need a service appointment and maybe a loaner."
    print(f"User: {sample}")
    for line in explain(sample):
        print(f"Glossary: {line}")


if __name__ == "__main__":
    main()
