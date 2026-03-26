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
from openai import OpenAI
from datetime import datetime
import json

client = OpenAI()


def get_current_time(format="%Y-%m-%d %H:%M:%S"):
    return datetime.now().strftime(format)


TOOLS = [{
    "type": "function",
    "name": "get_current_time",
    "description": "Get the current system time.",
    "parameters": {
        "type": "object",
        "properties": {
            "format": {
                "type": "string",
                "description": "Python date format (optional)."
            }
        },
        "required": []
    }
}]

FUNCTIONS = {
    "get_current_time": get_current_time
}


def query_model(prompt, model="gpt-4o-mini"):
    response = client.responses.create(
        model=model,
        input=prompt,
        tools=TOOLS,
    )

    while True:
        calls = [item for item in response.output if item.type == "function_call"]

        if not calls:
            return response.output_text

        outputs = []
        for call in calls:
            tool_name = call.name
            args = json.loads(call.arguments or "{}")
            print(f"\tTool requested: {tool_name}({args})")

            result = FUNCTIONS[call.name](**args)

            outputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": result,
            })

        response = client.responses.create(
            model=model,
            previous_response_id=response.id,
            input=outputs,
            tools=TOOLS,
        )


if __name__ == "__main__":
    prompt = "What time is it right now?"
    print("User:", prompt)
    print("Assistant:", query_model(prompt))
