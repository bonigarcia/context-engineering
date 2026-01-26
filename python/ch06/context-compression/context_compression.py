import os
from dotenv import load_dotenv

from llmlingua import PromptCompressor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


def word_count(text: str) -> int:
    return len(text.split())


def build_sample_conversation() -> str:
    # A deliberately long-ish conversation with specific facts that should survive compression.
    messages = [
        ("System", "You are a customer support assistant for Acme Gadgets."),
        ("User", "Hi, I need help with an order I placed last week."),
        ("Assistant", "Sure—can you share the order number and what seems to be the issue?"),
        ("User", "Order #A-10492. I ordered a NoiseCancel Pro headset and a USB-C dock."),
        ("Assistant", "Thanks. What’s the shipping address and preferred delivery instructions?"),
        ("User", "Ship to: John Smith, Calle de Alcalá 123, 28009 Madrid, Spain. Leave with the concierge if I'm not home."),
        ("Assistant", "Understood. Any issues with the items or the delivery timeline?"),
        ("User", "The dock arrived, but the headset didn’t. Tracking says delivered yesterday."),
        ("Assistant", "Sorry to hear that. Can you confirm the last four digits of the phone number on the order?"),
        ("User", "7788."),
        ("Assistant", "Thanks. I’ll open a missing item investigation. Do you want a replacement or a refund?"),
        ("User", "Replacement, please. Same model and color: black."),
        ("Assistant", "Noted. Also, do you want signature required for the replacement shipment?"),
        ("User", "Yes, require signature. And please send updates to boni@example.com."),
        ("Assistant", "Done. Anything else?"),
        ("User", "One more thing—if the headset can’t be shipped within 3 business days, switch to refund."),
        ("Assistant", "Confirmed: replacement preferred; refund if not shipped within 3 business days. Signature required."),
        ("User", "By the way, I love your products. I’ve bought several items over the years. "
                 "The dock is great, super fast, and the packaging was nice. "
                 "I’m just worried someone took the headset package."),
        ("Assistant", "Thanks for the feedback. We’ll investigate delivery details with the carrier."),
        ("User", "Also, could you remind me of the return policy? Not urgent, just curious."),
        ("Assistant", "Return policy is 30 days for most items in original condition. For now, I’ll prioritize the missing headset."),
    ]

    # Format into a single “conversation history” context block
    return "\n".join([f"{role}: {content}" for role, content in messages])


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Put it in your environment or a .env file."
        )

    # 1) Build sample conversation context
    conversation = build_sample_conversation()
    original_wc = word_count(conversation)

    print("\n--- Original Context ---")
    print(f"Original word count: {original_wc}")
    print(conversation)

    # 2) Compress with LLMLingua
    # You can override the compressor model via env var if needed.
    # The LLMLingua-2 model is a common default in examples.
    llmlingua_model = os.getenv(
        "LLMLINGUA_MODEL",
        "microsoft/llmlingua-2-xlm-roberta-large-meetingbank",
    )

    compressor = PromptCompressor(
        model_name=llmlingua_model,
        use_llmlingua2=True,
        device_map="cpu",
    )

    # Rate is the retained fraction (e.g., 0.33 keeps ~33%).
    # force_tokens helps preserve structure and question marks/newlines.
    compressed = compressor.compress_prompt(
        conversation,
        rate=float(os.getenv("LLMLINGUA_RATE", "0.33")),
        force_tokens=["\n", "?", "#", ":"],
    )

    # compress_prompt() may return either a string or a dict depending on version/config
    if isinstance(compressed, dict):
        compressed_text = compressed.get("compressed_prompt", "")
    else:
        compressed_text = str(compressed)

    compressed_wc = word_count(compressed_text)

    print("\n--- Compressed Context (LLMLingua) ---")
    print(f"Compressed word count: {compressed_wc}")
    print(compressed_text)

    # 3) Ask a question using the compressed context
    question = (
        "Summarize the customer’s request and provide the exact replacement/refund rules "
        "and delivery instructions (address + signature requirement + notification email)."
    )

    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
        api_key=api_key,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a precise support assistant. Use ONLY the provided context. "
                "If a detail is missing, say you don't know.",
            ),
            ("human", "Context:\n{context}\n\nQuestion:\n{question}"),
        ]
    )

    response = llm.invoke(
        prompt.format_messages(context=compressed_text, question=question)
    )

    # 4) Print final answer
    print("\n--- Final Answer (using compressed context) ---")
    print(response.content)


if __name__ == "__main__":
    main()
