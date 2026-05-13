# System prompt with Ollama models

This example demonstrates how to set up an [Ollama](https://ollama.com/) model and send a system prompt with JavaScript.

## Requirements

* [Node.js](https://nodejs.org/) 18+
* [Ollama](https://ollama.com/) running locally

## Steps for running this example in the shell

1. Run the script:
```bash
npm start
```

## Output

When you run the script, it will send a system prompt and a user prompt to the model, which should provide a response:

```
=== With system instructions ===
        Model: gemma3:4b
        Latency: 8.842 seconds
        Input tokens: 45
        Output tokens: 25
        Total tokens: 70
User query: Explain me what is context engineering in simple words
Response: Context engineering involves carefully designing and managing the information a language model needs to understand a prompt and generate a relevant response accurately.

=== With only user prompt ===
        Model: gemma3:4b
        Latency: 52.551 seconds
        Input tokens: 18
        Output tokens: 646
        Total tokens: 664
User query: Explain me what is context engineering in simple words
Response: Okay, let's break down "context engineering" in simple terms.

**Basically, it's about teaching AI (like chatbots or search engines) to *really* understand what you mean, not just the words you type.**

Here's a breakdown with an analogy:

**Imagine you're talking to a friend:**

* **Traditional AI:**  If you say "It's cold in here," a traditional AI might just look for the words "cold" and "here" and try to find a website about temperature or a place with a heater. It doesn't understand you're *complaining* about the temperature.
* **Context Engineering AI:** A context engineering AI would understand that you're likely in a room, it's probably winter, and you're expressing a feeling of discomfort. It would then respond with things like "Would you like me to turn up the thermostat?" or "Do you want me to find a blanket?"

**Here's how it works in practice:**

1. **Gathering Context:** The AI doesn't just look at the *current* question. It tries to build a picture of the situation by:
   * **Looking at the previous turns in the conversation:** (Like remembering what you just said).
   * **Understanding your intent:**  What are you *trying* to achieve? (e.g., find a restaurant, get directions, solve a problem).
   * **Considering the user's background:** (If possible - like knowing you're a frequent traveler).
   * **Analyzing the surrounding information:** (Like the time of day, location, or current events).

2. **Using that Context to Improve Responses:**  With all this context, the AI can give you much more relevant and helpful answers.

**Think of it like this:**  Context engineering is like giving the AI a really good "understanding of the situation" before it answers.


**Why is it important?**

* **Better Chatbots:** Makes chatbots feel more natural and helpful.
* **More Accurate Search Results:**  Helps search engines understand your *intent* behind your query, not just the keywords.
* **More Personalized Experiences:**  Allows AI to tailor responses to your specific needs and preferences.



**Resources to learn more:**

* **Towards Data Science - Context Engineering:** [https://towardsdatascience.com/context-engineering-a-new-approach-to-ai-understanding-79438898988](https://towardsdatascience.com/context-engineering-a-new-approach-to-ai-understanding-79438898988)
* **Wikipedia - Contextual AI:** [https://en.wikipedia.org/wiki/Contextual_AI](https://en.wikipedia.org/wiki/Contextual_AI)


Do you want me to delve into a specific aspect of context engineering, like:

*   How it relates to Large Language Models (LLMs)?
*   Different techniques used in context engineering?
```
