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

import json
from pathlib import Path

from jinja2 import Environment, StrictUndefined

ROOT = Path(__file__).resolve().parent
ENVIRONMENT = Environment(undefined=StrictUndefined, autoescape=False, trim_blocks=True, lstrip_blocks=True)


def load_template() -> str:
    return (ROOT / "prompt_template.j2").read_text(encoding="utf-8")


def load_cases() -> list[dict[str, str]]:
    return json.loads((ROOT / "test_cases.json").read_text(encoding="utf-8"))


def render_prompt(template: str, context: dict[str, str]) -> str:
    return ENVIRONMENT.from_string(template).render(**context)
