import torch
import time
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Optional, Tuple

# A type hint for the KV cache structure.
PastKeyValues = Tuple[Tuple[torch.Tensor, torch.Tensor], ...]

class TrueCacheAugmentedGenerator:
    """
    A minimal implementation of cache-augmented generation (cache-AG).

    This class implements the generation loop to provide a demonstration
    of how the Key-Value (KV) cache is created, injected, and updated.
    """
    def __init__(self, model_name: str = "gpt2"):
        """Initializes the model and tokenizer."""
        print(f"Loading model: {model_name}...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Running on device: {self.device}")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)
        self.tokenizer.pad_token = self.tokenizer.eos_token

        # Internal state for the cache
        self.kv_cache: Optional[PastKeyValues] = None

    def preload_context(self, context: str):
        """
        Phase 1: "Remembering"
        Processes the context and stores its computed state in the KV cache.
        This is done only once and is the more expensive step.
        """
        print(f"\n--- [Phase 1] Pre-loading context... ---")
        start_time = time.time()

        inputs = self.tokenizer(context, return_tensors="pt").to(self.device)
        
        # Perform a single forward pass to generate and store the KV cache.
        # The model internally calculates and returns the cache when `use_cache=True`.
        with torch.no_grad():
            outputs = self.model(**inputs, use_cache=True)
        
        self.kv_cache = outputs.past_key_values
        
        elapsed = (time.time() - start_time) * 1000
        print(f"Context ingested and cached in {elapsed:.2f}ms.")

    def ask(self, query: str, max_new_tokens: int = 50) -> str:
        """
        Phase 2: "Querying" using a manual generation loop.
        This is the fast, cheap step that reuses the cached context.
        """
        if self.kv_cache is None:
            raise ValueError("You must call `preload_context` before asking a question.")

        print(f"\n--- [Phase 2] Answering query: '{query}' ---")
        start_time = time.time()

        # 1. Start with the tokenized query as the initial input.
        input_ids = self.tokenizer(query, return_tensors="pt").to(self.device).input_ids
        
        # Use the pre-computed cache from the context.
        current_cache = self.kv_cache
        generated_token_ids = []

        # 2. Manual auto-regressive generation loop
        for _ in range(max_new_tokens):
            with torch.no_grad():
                # Forward pass: provide the current token(s) and the latest cache.
                outputs = self.model(
                    input_ids=input_ids,
                    past_key_values=current_cache,
                    use_cache=True
                )
            
            # 3. Get the predicted next token (greedy decoding)
            next_token_logits = outputs.logits[:, -1, :]
            next_token_id = torch.argmax(next_token_logits, dim=-1).unsqueeze(-1)
            
            # 4. Store the generated token
            generated_token_ids.append(next_token_id.item())

            # 5. Stop if the End-Of-Sentence token is generated
            if next_token_id.item() == self.tokenizer.eos_token_id:
                break
            
            # 6. Update the cache and prepare input for the next iteration
            current_cache = outputs.past_key_values
            input_ids = next_token_id # The next input is just the token we just generated

        elapsed = (time.time() - start_time) * 1000
        print(f"Query processed in {elapsed:.2f}ms via manual generation loop.")

        # Decode the generated tokens into a string
        return self.tokenizer.decode(generated_token_ids, skip_special_tokens=True)

if __name__ == "__main__":
    generator = TrueCacheAugmentedGenerator(model_name="gpt2")

    science_facts = (
        "Jupiter is the largest planet in our solar system. Its mass is "
        "two and a half times that of all the other planets in the Solar System combined. "
        "Mitochondria are membrane-bound cell organelles that generate most of "
        "the chemical energy needed to power the cell's biochemical reactions."
    )
    generator.preload_context(science_facts)

    questions = [
        "What is the function of mitochondria?",
        "How massive is Jupiter?",
    ]

    for q in questions:
        answer = generator.ask(q)
        print(f"  - User: {q}")
        print(f"  - AI: {answer}\n")

    # Asking a new question demonstrates the cache is being reused
    print("--- Asking another question to show cache reusability ---")
    new_question = "Which planet is the most massive in our solar system?"
    answer = generator.ask(new_question)
    print(f"  - User: {new_question}")
    print(f"  - AI: {answer}\n")
