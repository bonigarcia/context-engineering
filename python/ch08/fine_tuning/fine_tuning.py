from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling
import torch
import os

def fine_tune():
    model_name = "distilgpt2"
    data_file = "medical_data.txt"
    output_dir = "./medical_assistant_model"

    print(f"[INFO] Loading tokenizer and model: {model_name}")
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Prepare dataset for training
    def tokenize_function(examples):
        return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)

    from datasets import load_dataset
    dataset = load_dataset("text", data_files={"train": data_file})
    tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=["text"])

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    print("[INFO] Configuring trainer...")
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=50,
        per_device_train_batch_size=2,
        save_steps=100,
        logging_steps=10,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        data_collator=data_collator,
    )

    print("[INFO] Starting fine-tuning (this may take a few minutes)...")
    trainer.train()

    print(f"[INFO] Saving model to {output_dir}")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)

    # Test the model
    print("[INFO] Testing fine-tuned model...")
    input_text = "Question: What should I do for a mild headache? Answer:"
    # Use padding and truncation for the test input to get a proper attention mask
    inputs = tokenizer(input_text, return_tensors="pt", padding=True)
    
    outputs = model.generate(
        inputs["input_ids"], 
        attention_mask=inputs["attention_mask"],
        max_length=50, 
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=2
    )
    print("Generated Output:")
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))

if __name__ == "__main__":
    fine_tune()