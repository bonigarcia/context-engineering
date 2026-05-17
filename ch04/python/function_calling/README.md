# Function calling

This example demonstrates the *function-calling* pattern using an [OpenAI](https://openai.com/) GPT model. In this pattern, the model can call external functions to get information. The model decides when it needs external data, calls a function, and then uses the function result to answer.

## Requirements

* [Python](https://www.python.org/) 3.6+
* An [OpenAI API key](https://platform.openai.com/api-keys)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
python -m venv .venv

# macOS/Linux:
source .venv/bin/activate

# Windows Command Prompt:
.venv\Scripts\activate.bat

# Windows PowerShell:
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

2. Export your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="sk-..." # Windows cmd: set OPENAI_API_KEY="sk-..." # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
```

3. Run the script:
```bash
python function_calling.py
```

## Output

When you run the script, it will send a fixed user prompt (`What is the weather in San Francisco?`) to a GPT model (`gpt-4o-mini`). The model will determine that it needs to call the `get_weather` function to answer the question, and it will do so with the specified format. The application will execute the function, and inject it back into the conversation as a `tool` message. Finally, the model will produce a user-facing answer grounded in the tool result.

```
User: What is the weather in San Francisco?
== 1. TOKEN COUNTING ==
Estimated input tokens: 47

== 2. INITIAL MODEL RESPONSE ==
Raw response output items:

[1] type=reasoning
        {
  "id": "rs_06b90d62f130acdc0069c92dc38f2881909fa9550ca5d33439",
  "summary": [],
  "type": "reasoning",
  "content": null,
  "encrypted_content": null,
  "status": null
}

[2] type=function_call
        {
  "arguments": "{\"location\":\"San Francisco\"}",
  "call_id": "call_nYxqZbtp6ZFUBItKdwE8vaQm",
  "name": "get_weather",
  "type": "function_call",
  "id": "fc_06b90d62f130acdc0069c92dc50ad0819087946c20bc0d163a",
  "namespace": null,
  "status": "completed"
}

== 3. FUNCTION CALLING ==
Function name : get_weather
Arguments     : {
  "location": "San Francisco"
}
Function result:
{
  "location": "San Francisco",
  "temperature_c": 18,
  "condition": "Sunny",
  "humidity_percent": 63
}

== 4. FINAL MODEL RESPONSE ==
GPT: The current weather in San Francisco is sunny with a temperature of 18°C and a humidity level of 63%.
```