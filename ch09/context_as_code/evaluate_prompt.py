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

from openai import OpenAI

from prompt_engine import load_cases, load_template, render_prompt


MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

PROMPT_CONTEXT = {
    "role": "support triage assistant",
    "company_name": "Acme Support",
    "urgent_label": "urgent",
    "normal_label": "normal",
}


def classify_ticket(client: OpenAI, template: str, ticket: str) -> str:
    prompt = render_prompt(template, {**PROMPT_CONTEXT, "ticket": ticket})
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip().lower()


def main() -> None:
    client = OpenAI()
    template = load_template()
    cases = load_cases()

    passed = 0
    print(f"[INFO] Evaluating prompt template with {MODEL}...")

    for case in cases:
        actual = classify_ticket(client, template, case["ticket"])
        expected = case["expected"]
        ok = actual == expected
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {case['name']}: expected={expected}, actual={actual}")
        if ok:
            passed += 1

    print(f"[INFO] Passed {passed}/{len(cases)} checks.")
    if passed != len(cases):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
