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

REVIEW_PROMPT = """You are a senior code reviewer. Given a code diff, analyze the change and return structured feedback.

Check each file for:
- Correctness: edge cases, error handling, logic errors
- Security: injection risks, exposed secrets, unsafe patterns
- Maintainability: naming clarity, function focus, complexity
- Style: language conventions

Return a JSON object with:
- files_reviewed (list of file paths)
- findings (list of objects with severity: critical/warning/info, description, file, line)
- summary (brief overall assessment and recommended action)"""

app = BedrockAgentCoreApp()
client = boto3.client("bedrock-runtime")


@app.entrypoint
def review(payload):
    diff = payload.get("diff", "")
    if not diff:
        return {"result": "No diff provided"}
    messages = [
        {"role": "system", "content": [{"text": REVIEW_PROMPT}]},
        {"role": "user", "content": [{"text": f"Review this diff:\n\n{diff}"}]},
    ]
    response = client.converse(modelId=MODEL_ID, messages=messages)
    message = response["output"]["message"]["content"][0]["text"]
    return {"review": message}


if __name__ == "__main__":
    app.run()