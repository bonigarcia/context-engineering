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

import boto3
from bedrock_agentcore.runtime import BedrockAgentCoreApp

MODEL_ID = "anthropic.claude-sonnet-4-5-20250929-v1:0"

# The runtime exposes the agent through a managed HTTP entrypoint
app = BedrockAgentCoreApp()
client = boto3.client("bedrock-runtime")


@app.entrypoint
def invoke(payload):
    user_message = payload.get("prompt", "Hello")
    messages = [{"role": "user", "content": [{"text": user_message}]}]
    response = client.converse(modelId=MODEL_ID, messages=messages)
    message = response["output"]["message"]["content"][0]["text"]
    return {"result": message}


if __name__ == "__main__":
    app.run()
