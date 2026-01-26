import os
from openai import OpenAI
from dotenv import load_dotenv

def get_user_input(prompt):
    """Get input from the user."""
    return input(prompt)

def main():
    """
    Main function to run the human-in-the-loop story writing assistant.
    """
    load_dotenv()

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    print("--- Collaborative Story Writing Assistant ---")
    print("You and the AI will write a story together.")
    print("Type 'quit' or 'exit' at any time to end the story.")
    print("\n")

    # Initial prompt from the user
    story_context = get_user_input("To start, what should the story be about? ")
    if story_context.lower() in ["quit", "exit"]:
        return

    messages = [
        {"role": "system", "content": "You are a creative writing assistant. You write short, compelling story paragraphs based on the user's guidance. The user is in the loop to approve or modify the story as it develops."},
        {"role": "user", "content": f"Let's start a story. Here is the premise: {story_context}"}
    ]
    full_story = [story_context]

    while True:
        # Get AI's continuation
        print("\n... The AI is thinking ...\n")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        ai_paragraph = response.choices[0].message.content
        print("--- AI's suggestion ---")
        print(ai_paragraph)
        print("-----------------------")

        # Human-in-the-loop feedback
        feedback = get_user_input("What happens next? (Approve with Enter, or provide a different direction): ")

        if feedback.lower() in ["quit", "exit"]:
            break
        
        # Append the AI-generated part and the user's new direction
        messages.append({"role": "assistant", "content": ai_paragraph})
        full_story.append(ai_paragraph)

        if feedback:
            # If user provides feedback, add it to the messages for the next turn
            messages.append({"role": "user", "content": feedback})
            full_story.append(f"[{feedback}]") # Add feedback to the story for clarity
        else:
            # If user just approves, ask the AI to continue
             messages.append({"role": "user", "content": "Continue the story."})

    print("\n--- Your Final Story ---")
    print("\n".join(full_story))

if __name__ == "__main__":
    main()
