# Semantic Kernel tool use

Tool: `lookup_example_code`

Purpose:
- Return a fixed code word so the plugin call is easy to verify.

Behavior:
- If the user asks `What is the example code word?`, return `SK-TOOL-42`.
- If the request is outside that scope, do not use the tool.

Verification prompt:
- Ask: `What is the example code word?`
- Expected tool result: `SK-TOOL-42`
