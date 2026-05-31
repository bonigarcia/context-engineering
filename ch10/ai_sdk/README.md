# AI SDK

This chapter slice shows small Vercel AI SDK examples that all run offline with mock models.

## Included examples

- `basic_text_generation/`: a runnable `generateText()` example using `MockLanguageModelV3` from `ai/test`
- `streaming_text/`: a runnable `streamText()` example that streams text from a mock model
- `structured_output/`: a runnable structured-output example using `Output.object()` and Zod
- `tool_use/`: a runnable multi-step tool example using `tool()` and a mock tool call

## Run the example

Each example is self-contained:

```bash
cd ch10/ai_sdk/<example-folder>
npm install
npm start
```
