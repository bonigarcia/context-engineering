# Basic interaction with Google Gemini models

This example demonstrates how to set up a [Google Gemini](https://gemini.google.com/) model and send a basic user prompt with JavaScript.

## Requirements

* [Node.js](https://nodejs.org/)
* A [Gemini key](https://aistudio.google.com/)

## Steps for running this example in the shell

1.  Install dependencies:
```bash
npm install
```

2. Export your Gemini API key as an environment variable:
```bash
export GEMINI_API_KEY="..." # Windows cmd: set GEMINI_API_KEY="..." # Windows PowerShell: $env:GEMINI_API_KEY="..."
```

3. Run the script:
```bash
npm start
```

## Output

When you run the script, it will send a user prompt to a Gemini model (`gemini-2.5-flash`). Then, it will send the same user prompt to a more advanced model (`gemini-3.5-flash-lite`). The output will show the responses from both models.
The transcript below was captured with earlier releases of these models. Model identifiers, latency, token counts, and wording will differ on each run.


```
=== Basic model  ===
User: How many tokens are in your context window?
        Latency: 4.006 seconds
        Prompt tokens: 10
        Output tokens: 233
        Thinking tokens: 469
        Total tokens: 712
Gemini-2.5: As a large language model, I don't have a fixed, self-aware "context window" in the way a human might. My context window is a technical parameter of the underlying model architecture and the specific API or deployment I'm running on.

The context window size for models like me (and specifically for Google's Gemini family of models, which I am a part of) can vary significantly. It's often expressed in thousands of tokens.

For example, some versions of Gemini models offer context windows ranging from:

*   **8,192 tokens**
*   **32,768 tokens**
*   **128,000 tokens**
*   And even larger, with some specialized versions or future iterations potentially reaching **1 million tokens** or more.

The exact number depends on the specific model version (e.g., Gemini 1.0 Pro, Gemini 1.5 Pro, Gemini 1.5 Flash) and the API endpoint being used. I don't have real-time access to query the precise context window of my current operational instance.
=== Advanced model  ===
User: How many tokens are in your context window?
        Latency: 0.784 seconds
        Prompt tokens: 10
        Output tokens: 21
        Thinking tokens: undefined
        Total tokens: 31
Gemini-3.5: My context window is **128,000 tokens** (for both input and output).
```