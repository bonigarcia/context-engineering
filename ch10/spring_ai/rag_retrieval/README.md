# Retrieval with Spring AI and Ollama

This example shows a tiny local RAG flow using Spring AI, Ollama embeddings, and an in-memory vector store.

It indexes a few short notes, retrieves the best match, and asks the chat model to answer from that context.

## Requirements

* [Java](https://www.oracle.com/java/technologies/downloads/) 21+
* [Maven](https://maven.apache.org/) 3.9+
* [Ollama](https://ollama.com/) installed locally
* A pulled chat model such as `llama3.2:1b`
* A pulled embedding model such as `nomic-embed-text`

## Steps for running this example in the shell

1. Start Ollama and pull the chat model:
```bash
ollama serve
ollama pull llama3.2:1b
ollama pull nomic-embed-text
```

2. Run the application:
```bash
mvn spring-boot:run
```

## Output

```
User: How do I reset my password?
Model: It seems like you're trying to reset your password using the self-service portal and then sign in again. Here's a step-by-step guide to help you with that:

**Resetting your password using the self-service portal:**

1. Go to the [Company Website](http://www.companywebsite.com) or [Your Company's Self-Service Portal](http://yourcompanyportal.com).
2. Log in to your account using your username and password.
3. Click on the "Forgot Password" or "Reset Password" link.
4. Enter your email address or username and click "Submit".
5. Follow the prompts to reset your password. You may be asked to provide additional security questions or confirm your new password.

**Signing in again after resetting your password:**

1. Go back to the self-service portal (or your company's portal).
2. Enter your new password and confirm it.
3. Click "Sign In" to access your account.

Alternatively, if you're trying to sign in using the local VPN client, make sure you have the correct login credentials and have previously configured your VPN settings to use the office profile.
```
