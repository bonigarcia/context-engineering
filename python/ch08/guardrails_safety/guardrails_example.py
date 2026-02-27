from pydantic import BaseModel, Field
from guardrails import Guard
from guardrails.hub import ProfanityFree
import json

# 1. Define the schema for the model's output
# We use Pydantic to specify the expected structure and validation rules.
# For Pydantic V2, we use json_schema_extra to pass custom metadata like validators.
class AgentResponse(BaseModel):
    summary: str = Field(
        description="A concise summary of the user's request.",
        # Guardrails expects validators in the metadata
        json_schema_extra={
            "validators": [ProfanityFree(on_fail="fix")]
        }
    )
    confidence: float = Field(
        description="The confidence score for the summary.",
        ge=0.0,
        le=1.0
    )

def main():
    # 2. Initialize the Guard object with the Pydantic schema
    guard = Guard.for_pydantic(AgentResponse)

    # 3. Simulate a raw LLM output
    raw_llm_output = (
        '{"summary": "The system is working perfectly and the context is clear.", '
        '"confidence": 0.95}'
    )

    # 4. Parse and validate the output
    print("Validating LLM output...")
    response = guard.parse(raw_llm_output)

    if response.validation_passed:
        print("Validation successful!")
        print(f"Validated Output: {response.validated_output}")
    else:
        print("Validation failed.")
        print(f"Errors: {response.validation_summaries}")

    # 5. Example of a failed validation
    # We use a word likely to be caught by a standard profanity filter
    print("\nSimulating failed validation (content check)...")
    bad_output = (
        '{"summary": "The system is absolute crap and failing.", '
        '"confidence": 0.1}'
    )
    
    # The 'fix' action would attempt to mask or remove the offending words
    response_fail = guard.parse(bad_output)
    
    if not response_fail.validation_passed:
         print("Validation failed as expected.")
    
    print(f"Cleaned Output: {response_fail.validated_output}")

if __name__ == "__main__":
    main()
