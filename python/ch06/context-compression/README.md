# Context compression with LLMLingua

This example demonstrates the concept of **Context Compression** using the `LLMLingua` library. It shows how to compress a long conversation history to reduce its token count while preserving essential semantic information.

## Requirements

This project requires [Python](https://www.python.org/) 3.6+ and the libraries listed in `requirements.txt`.

## Steps for running this example

1.  Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

2. Set environment variables:
Ensure your OpenAI API key is set as an environment variable. You can do this by:
```
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
```
Alternatively, create a `.env` file in the source directory with the content `OPENAI_API_KEY="YOUR_OPENAI_API_KEY"`.

3. Run the script:
```bash
python context_compression.py
```

## Output

When you run the script, it will:

1. Print the original word count of the sample conversation.
2. Display the compressed version of the context and its new, lower word count.
3. Use the compressed context to ask a question to an LLM.
4. Print the final answer from the LLM, demonstrating that the key information was successfully retained during compression.
