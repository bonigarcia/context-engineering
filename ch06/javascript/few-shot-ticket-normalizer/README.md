# Few-shot ticket normalizer

This example demonstrates few-shot prompting by transforming an unstructured bug report into a normalized support ticket schema.

The prompt includes a small set of labeled examples, then asks the model to apply the same pattern to a new report.

## Requirements

* [Node.js](https://nodejs.org/)
* An [OpenAI API key](https://platform.openai.com/api-keys)

## Steps for running this example in the shell

1. Install dependencies:
```bash
npm install
```

2. Export your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY="sk-..." # Windows cmd: set OPENAI_API_KEY="sk-..." # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
```

3. Run the script:
```bash
npm start
```

## Output

When you run the script, it will print the input bug report and the normalized ticket returned by the model.
