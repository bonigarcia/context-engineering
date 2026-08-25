# Streaming responses from Google Gemini models

This example demonstrates how to stream the response of a [Google Gemini](https://gemini.google.com/) model with JavaScript. Instead of waiting for the complete answer, the script prints each fragment as the model produces it and reports the time to first token.

## Requirements

* [Node.js](https://nodejs.org/) 18+
* A [Google API key](https://aistudio.google.com/)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
npm install
```

2. Export your API key as an environment variable:
```bash
export GOOGLE_API_KEY="..." # Windows cmd: set GOOGLE_API_KEY="..." # Windows PowerShell: $env:GOOGLE_API_KEY="..."
```

3. Run the script:
```bash
npm start
```

## Output

When you run the script, it sends a user prompt to a Gemini model (`gemini-2.5-flash`) and prints the answer as it is generated. Once the stream ends, it prints the time to first token, the total latency, and the token counts. This example uses the current `@google/genai` SDK. Each streamed chunk can carry usage metadata, so the script keeps the last one it sees and reports it after the stream ends.
