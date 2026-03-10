from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def query_model(user_prompt: str, model: str = "gpt-4.1-mini", temperature: float = 0) -> str:
    """Send a text prompt to an OpenAI model and return the text response."""

    # Create the client (it reads the API key from the OPENAI_API_KEY env)
    client = OpenAI()

    # Send the request
    response = client.responses.create(
        model=model,
        input=user_prompt,
        temperature=temperature,
    )

    return response.output_text

if __name__ == "__main__":
    user_prompt = "How many tokens is your context window?"
    response = query_model(user_prompt)
    print("User:", user_prompt)
    print("AI:", response)