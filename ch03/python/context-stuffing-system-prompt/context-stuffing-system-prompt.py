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

# Setup OpenAI client
client = OpenAI()

def query_model(system_message: str,
                user_message: str,
                model: str = "gpt-4o-mini",
                max_tokens: int = 1024) -> str:
    """Send a system + user message pair to a model."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content

manual_text = """# Contoso Barista Pro 3000 – Maintenance & Troubleshooting Guide

This document describes key procedures for safely operating, cleaning, and troubleshooting
the Contoso Barista Pro 3000 espresso machine.

## 1. Daily operation

- Allow the machine to warm up for at least 15 minutes before brewing.
- Always use filtered water to reduce scale buildup.
- Do not run the pump without water in the reservoir.

## 2. Descaling procedure

1. Turn off the steam function and let the machine cool down for at least 20 minutes.
2. Empty the drip tray and remove the portafilter.
3. Fill the water reservoir with a descaling solution according to the manufacturer’s instructions.
4. Run a cleaning cycle until the reservoir is half empty.
5. Let the machine rest for 10 minutes so the descaling solution can dissolve mineral deposits.
6. Finish the cleaning cycle and then rinse the reservoir thoroughly with fresh water.
7. Run two full tanks of fresh water through the system before brewing coffee again.

## 3. Steam wand cleaning

- After every use, wipe the steam wand with a damp cloth.
- Purge steam for 3–5 seconds to clear residual milk.
- Once per week, soak the tip of the steam wand in warm water with a food-safe detergent.

## 4. Error codes

- **E10**: Water reservoir is empty or not seated correctly.
- **E12**: Pump is overheated. Turn off the machine and wait 30 minutes before restarting.
- **E17**: Descale cycle incomplete. The machine detected residual descaling solution or scale.
- **E32**: Temperature sensor fault. Contact a qualified service technician.

## 5. Resolving error code E17

1. Confirm that the descaling procedure from Section 2 was completed, including both rinse cycles.
2. Inspect the water reservoir and ensure it is filled with fresh water only.
3. Run one additional rinse cycle with fresh water.
4. If the error persists, unplug the machine for 5 minutes and restart it.
5. If E17 still appears, contact customer support with the machine’s serial number.

## 6. Safety notes

- Never open the machine housing while it is connected to power.
- Hot surfaces and pressurized steam can cause burns.
- Always allow the machine to cool completely before performing internal maintenance.
"""

base_instructions = """You are a support assistant for the Contoso Barista Pro 3000 espresso machine.

Use ONLY the information in the reference manual below to answer questions.
If the manual does not contain the answer, say that the information is not available.
Explain your reasoning in clear, step-by-step language that a non-expert user can follow.
When possible, refer to relevant sections of the manual by name or number.
"""

def build_system_message_with_manual() -> str:
    """Construct a system message that includes both role instructions
    and the full reference manual.
    """
    system_message = f"""{base_instructions}

====================
REFERENCE MANUAL
====================
{manual_text}
"""
    return system_message

if __name__ == "__main__":
    system_message = build_system_message_with_manual()
    
    example_question = "The machine shows error code E17 after I finished descaling. What should I do?"
    print(f"User: {example_question}")
    
    response = query_model(system_message, example_question)
    print(f"\nResponse:\n{response}")
