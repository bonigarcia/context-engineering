# Stateful ticket with Spring AI and Ollama

This example shows the **State** context source — session-scoped state that
persists across turns via a ticket tracking system.

A concurrent HashMap holds ticket state (status, description) per
conversation. The ChatClient reads and transitions state through tools.

## Requirements

* Java 21+, Maven 3.9+, Ollama with `llama3.2:3b`

## Steps

```
ollama serve
ollama pull llama3.2:3b
mvn spring-boot:run
```

## Output

```
User: Create a ticket for a broken laptop
Model: I have created a new ticket for you. The ticket details are as follows:

* Ticket #1
* Description: broken laptop
* Status: open

I will investigate this matter further and keep you updated on the status of your ticket.

User: I've replaced the screen, it works now
Model: Ticket #1 has been updated to reflect the resolution. I'll make sure to note this in the ticket details:

* Ticket #1
* Description: broken laptop (resolved after screen replacement)

User: What is the status of my ticket?
Model: The current status of your ticket is "resolved".

User: Everything is fixed
Model: I have updated the ticket status to "resolved".
```