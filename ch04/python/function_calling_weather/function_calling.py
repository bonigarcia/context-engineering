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
import json
from typing import Any, Dict
from openai import OpenAI

client = OpenAI()  # OPENAI_API_KEY should be set as an environment variable


# -----------------------------
# Local function implementation
# -----------------------------
def get_weather(location: str) -> Dict[str, Any]:
    """
    Mock weather lookup used only for demonstration.

    In a real app, this function would call your own weather provider or backend.
    """
    fake_weather_db = {
        "san francisco": {
            "location": "San Francisco",
            "temperature_c": 18,
            "condition": "Sunny",
            "humidity_percent": 63,
        },
        "new york": {
            "location": "New York",
            "temperature_c": 12,
            "condition": "Cloudy",
            "humidity_percent": 71,
        },
        "london": {
            "location": "London",
            "temperature_c": 10,
            "condition": "Light rain",
            "humidity_percent": 82,
        },
    }

    key = location.strip().lower()
    result = fake_weather_db.get(
        key,
        {
            "location": location,
            "temperature_c": 21,
            "condition": "Unknown (demo data)",
            "humidity_percent": 50,
        },
    )
    return result


# -------------------------------------
# Function/tool schema sent to the model
# -------------------------------------
TOOLS = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get the current weather in a location",
        "parameters": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"],
        },
    }
]


def route_function_call(name: str, arguments: Dict[str, Any]) -> Any:
    """
    Dispatch model tool calls to local Python functions.
    """
    if name == "get_weather":
        return get_weather(arguments["location"])
    raise ValueError(f"Unknown function requested by model: {name}")


def query_model(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Send a user prompt with tools to an OpenAI model and return the text response.
    """

    # ------------------------------------------------
    # Step 1: Count tokens for the exact request shape
    # ------------------------------------------------
    # Tool definitions (function schemas, MCP servers, etc.) add tokens to the context.
    # We can count them together with the user prompt as follows:
    # https://developers.openai.com/api/docs/guides/token-counting
    token_count = client.responses.input_tokens.count(
        model=model,
        tools=TOOLS,
        input=prompt,
    )
    print("== 1. TOKEN COUNTING ==")
    print(f"Estimated input tokens: {token_count.input_tokens}\n")

    # ----------------------------------------------------------
    # Step 2: Send the request and force at least one tool call
    # ----------------------------------------------------------
    # OpenAI documents that tool_choice can be "auto", "required", "none",
    # or a specific function. We use "required" here so the demo reliably
    # exercises the function-calling path.
    response = client.responses.create(
        model=model,
        tools=TOOLS,
        tool_choice="required",
        input=prompt,
    )

    print("== 2. INITIAL MODEL RESPONSE ==")
    print("Raw response output items:")
    for i, item in enumerate(response.output, start=1):
        print(f"\n[{i}] type={item.type}")
        # Use model_dump() if available (Pydantic models), else fall back.
        if hasattr(item, "model_dump"):
            print(json.dumps(item.model_dump(), indent=2))
        else:
            print(item)
    print()

    # -----------------------------------------------------------------
    # Step 3: Preserve output items and execute any function calls found
    # -----------------------------------------------------------------
    # OpenAI's function-calling guide shows preserving the model's output
    # items, then appending a "function_call_output" item with the same call_id.
    input_items = list(response.output)

    for item in response.output:
        if item.type != "function_call":
            continue

        function_name = item.name
        function_args = json.loads(item.arguments)

        print("== 3. FUNCTION CALLING ==")
        print(f"Function name : {function_name}")
        print(f"Arguments     : {json.dumps(function_args, indent=2)}")
        result = route_function_call(function_name, function_args)
        print("Function result:")
        print(json.dumps(result, indent=2))
        print()

        # Send function result back to the model.
        input_items.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(result),
            }
        )

    # --------------------------------------------------------
    # Step 4: Ask the model for the final natural-language reply
    # --------------------------------------------------------
    final_response = client.responses.create(
        model=model,
        tools=TOOLS,
        input=input_items,
    )
    print("== 4. FINAL MODEL RESPONSE ==")
    return final_response.output_text


if __name__ == "__main__":
    user_prompt = "What is the weather in San Francisco?"
    print("User:", user_prompt)
    response = query_model(user_prompt)
    print("GPT:", response)
