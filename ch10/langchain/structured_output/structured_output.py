"""
(C) Copyright 2026 Boni Garcia (https://bonigarcia.github.io/)
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")


# Define the structure expected from the model
class CityAnswer(BaseModel):
    city: str = Field(description="Name of the capital city")
    country: str = Field(description="Country the city belongs to")


if __name__ == "__main__":
    # Initialize the chat model through the provider-agnostic factory
    model = init_chat_model("openai:gpt-5-mini", temperature=0)

    # Bind the schema so the model returns a validated object
    structured_model = model.with_structured_output(CityAnswer)
    answer = structured_model.invoke("What is the capital of France?")

    print(answer)
