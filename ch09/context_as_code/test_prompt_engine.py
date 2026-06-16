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
from importlib import util
from pathlib import Path


def load_module():
    path = Path(__file__).with_name("prompt_engine.py")
    spec = util.spec_from_file_location("prompt_engine", path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_render_prompt_injects_context():
    module = load_module()

    template = (
        "You are {{ role }} for {{ company_name }}.\n"
        "Label the ticket as {{ urgent_label }} or {{ normal_label }}.\n"
        "Ticket: {{ ticket }}"
    )
    result = module.render_prompt(
        template,
        {
            "role": "support triage assistant",
            "company_name": "Acme",
            "urgent_label": "urgent",
            "normal_label": "normal",
            "ticket": "Password reset",
        },
    )

    assert "support triage assistant" in result
    assert "Acme" in result
    assert "urgent" in result
    assert "normal" in result
    assert "Password reset" in result
