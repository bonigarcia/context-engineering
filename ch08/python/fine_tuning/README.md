# Fine-tuning: customizing model behavior

This example demonstrates how to fine-tune a small language model ([DistilGPT2](https://huggingface.co/distilbert/distilgpt2)) to adopt a specific professional persona using a small, specialized dataset.

## Requirements

This project requires [Python](https://www.python.org/) 3.x and the libraries listed in `requirements.txt`.

## Steps for running this example

1. Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows cmd: .venv\Scripts\activate # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

2. Run the script:
```bash
python fine_tuning.py
```

## Output

The script will prepare a small dataset of "Medical Assistant" interactions, configure the training arguments, and run a training loop (limited to 1 epoch for demonstration). It will then save the model and show a sample response.

```text
[INFO] Loading tokenizer and model: distilgpt2
[INFO] Configuring trainer...
...
[INFO] Saving fine-tuned model to ./medical_assistant_model
[INFO] Generating response from fine-tuned model:
Input: What should I do for a mild headache?
Output: As a Medical Assistant, I recommend resting in a quiet room and staying hydrated. If symptoms persist, please consult a physician.
```