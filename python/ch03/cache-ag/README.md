# Cache-augmented generation (cache-AG)

This sample application implements a minimal cache-AG system using the following stack:

-   **LLM**: [GPT-2](https://huggingface.co/gpt2)
-   **Libraries**: [PyTorch](https://pytorch.org/), [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)

This example demonstrates how to pre-load external knowledge into the model's internal Key-Value (KV) cache. It uses a manual generation loop to provide a view of how the cache is injected and updated.

### Requirements

To run this example, you only need [Python](https://www.python.org/) 3.x.

### Steps for running this example

1.  Navigate to the example directory:
    ```bash
    # Assuming you have cloned the repository
    cd python/ch03/cache-ag
    ```

2.  Create a virtual environment and activate it:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Run the Cache-AG example script:
    ```bash
    python3 cache_ag.py
    ```

### Output

After running the script, you will see the model being loaded, the context being cached, and then the model answering questions using that cache. The output should look similar to this:

```
Loading model: gpt2...
Running on device: cpu

--- [Phase 1] Pre-loading context... ---
Context ingested and cached in 153.66ms.

--- [Phase 2] Answering query: 'What is the function of mitochondria?' ---
Query processed in 1908.55ms via manual generation loop.
  - User: What is the function of mitochondria?
  - AI:  The mitochondria are the most important organelles in the body. They are responsible for the production of energy, which is why they are called "energy-producing" cells. The mitochondria are also responsible for the production of oxygen, which is

--- [Phase 2] Answering query: 'How massive is Jupiter?' ---
Query processed in 1846.99ms via manual generation loop.
  - User: How massive is Jupiter?
  - AI:  The largest planet in our solar system is about the size of Jupiter. It is about the size of the Earth. It is about the size of the Sun. It is about the size of the Moon. It is about the size of the Earth.

--- Asking another question to show cache reusability ---

--- [Phase 2] Answering query: 'Which planet is the most massive in our solar system?' ---
Query processed in 1891.84ms via manual generation loop.
  - User: Which planet is the most massive in our solar system?
  - AI:  The Earth is about the size of the Sun. It is about the size of the Moon. It is about the size of the Earth. It is about the size of the Sun. It is about the size of the Earth. It is about the
```
