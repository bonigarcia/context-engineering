import asyncio
import logging
import time

from google.adk.agents.llm_agent import Agent
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.adk.events import Event, EventActions
from google.genai.types import Content, Part

logging.basicConfig(level=logging.INFO)

APP_NAME = "state_example_app"
USER_ID = "state_user"
SESSION_ID = "state_session"
MODEL = "gemini-2.0-flash"

async def run_scenario():
    session_service = InMemorySessionService()

    # --- 1. GreetingAgent (output_key) Example ---
    print("--- Running GreetingAgent (output_key) Example ---")

    initial_state_greeting = {"user:login_count": 0, "task_status": "idle"}
    session_greeting = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=f"{SESSION_ID}_greeting", 
        state=initial_state_greeting
    )
    print(f"Initial state: {session_greeting.state}")

    # Define agent with output_key
    greeting_agent = Agent(
        name="Greeter",
        model=MODEL,
        instruction="Generate a short, friendly greeting.",
        output_key="last_greeting" # Save response to state['last_greeting']
    )

    runner_greeting = Runner(
        agent=greeting_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    user_message = Content(parts=[Part(text="Hello")])
    for event in runner_greeting.run_async(
        user_id=USER_ID, session_id=f"{SESSION_ID}_greeting", new_message=user_message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            print(f"Agent responded with: {event.content.parts[0].text!r}")
    
    updated_session_greeting = await session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=f"{SESSION_ID}_greeting")
    print(f"State after agent run: last_greeting = {updated_session_greeting.state.get('last_greeting')!r}")

    # --- 2. Manual State Update (EventActions) Example ---
    print("--- Running Manual State Update (EventActions) Example ---")

    session_manual = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=f"{SESSION_ID}_manual",
        state={"user:login_count": 0, "task_status": "idle"}
    )
    print(f"Initial state: {session_manual.state}")

    # Define State Changes
    current_time = int(time.time()) # Use int for timestamp for consistency
    state_changes = {
        "task_status": "active",  # Update session state
        "user:login_count": session_manual.state.get("user:login_count", 0) + 1,  # Update user state
        "user:last_login_ts": current_time,  # Add user state
        "temp:validation_needed": True  # Add temporary state (will be discarded)
    }

    # Create Event with Actions
    actions_with_update = EventActions(state_delta=state_changes)
    system_event = Event(
        invocation_id="inv_login_update",
        author="system",
        actions=actions_with_update,
        timestamp=current_time
    )

    # Append the Event (This updates the state)
    await session_service.append_event(session_manual, system_event)
    print("`append_event` called with explicit state delta.")

    # Check Updated State
    updated_session_manual = await session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=f"{SESSION_ID}_manual")
    
    task_status = updated_session_manual.state.get("task_status")
    login_count = updated_session_manual.state.get("user:login_count")
    last_login_ts = updated_session_manual.state.get("user:last_login_ts")
    temp_validation = updated_session_manual.state.get("temp:validation_needed") # This should be None

    print(f"State after event: task_status={task_status!r}, user:login_count={login_count!r}, user:last_login_ts={last_login_ts!r}")
    if temp_validation is None:
        print("As expected, temp state was not persisted: 'temp:validation_needed' not found.")
    else:
        print(f"Unexpected temp state value: {temp_validation!r}")


if __name__ == "__main__":
    asyncio.run(run_scenario())
