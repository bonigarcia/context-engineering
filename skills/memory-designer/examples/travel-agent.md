# Trip planner agent

The trip planner is a chat agent that helps users book business trips: flights, hotels, and trains. Users come back several times a month.

## Conversation

Each session starts with the system prompt and the tool definitions. The full chat history of the current session is sent on every turn. There is no limit on the number of turns.

## Memory

At the end of every session, the agent stores the full transcript of the session in a vector database (long-term memory). At the start of a new session, it retrieves the five most similar past transcripts and adds them to the context.

The agent does not store anything else between sessions. Users regularly complain that they have to repeat their seat preference (aisle or window), their dietary needs for flight meals, and their preferred hotel chain every time.

## Booking flow

A booking goes through these steps: collect trip details, search options, user selection, hold the reservation, payment, confirmation.

The agent does not keep the progress of a booking anywhere except in the chat history. On each turn, the model reads the history to work out which step it is on and which options the user selected. When a session is interrupted (the user closes the app during payment, or the connection drops), the booking has to start again from the first step.
