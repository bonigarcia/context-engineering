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

When you run the script, it will send a user prompt to a Gemini model (`gemini-2.5-flash`). Then, it will send the same user prompt to a more advanced model (`gemini-3.1-flash-lite-preview`). The output will show the responses from both models.

```
=== Basic model  ===
User: How many tokens is your context window?
        Latency: 4.481 seconds
        Prompt tokens: 9
        Output tokens: 306
        Thinking tokens: 480
        Total tokens: 795
Gemini-2.5: As a large language model, I don't have a "context window" in the same way a human or a specific software application does. My capabilities are determined by the underlying model architecture.

However, the models I am based on (like various versions of Google's Gemini models) have different maximum input sizes, often referred to as "context windows" or "token limits" for a single API call. These limits can vary significantly:

*   Some models might have a context window of **32,768 tokens**.
*   Others might support **128,000 tokens**.
*   And some advanced versions are designed for even larger contexts, potentially up to **1 million tokens** or more for specific tasks.

**What does this mean for you?**

*   **Tokens** are not strictly words; they can be parts of words, punctuation, or spaces. A good rule of thumb is that 1,000 tokens are roughly 750 words in English.
*   The context window determines how much information (your prompt, previous turns of a conversation, retrieved documents) the model can "see" and process at one time to generate a response.
*   The exact limit depends on the specific model version and API you might be interacting with if you were building an application.

For most conversational interactions, the effective context is managed to ensure a coherent and relevant discussion, even if the underlying model can handle much larger inputs.
=== Advanced model  ===
User: How many tokens is your context window?
        Latency: 1.295 seconds
        Prompt tokens: 9
        Output tokens: 93
        Thinking tokens: 142
        Total tokens: 244
Gemini-3.1: I am a large language model, trained by Google.

My context window size depends on the specific version of the model you are interacting with. Currently, many versions of Gemini (such as Gemini 1.5 Pro) support a context window of **up to 2 million tokens**.

This allows me to process and "remember" a vast amount of information in a single conversation, including long documents, large codebases, or hours of video and audio.
```