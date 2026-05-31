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

import asyncio

import parlant.sdk as p


async def main() -> None:
    async with p.Server(nlp_service=p.NLPServices.openai) as server:
        agent = await server.create_agent(
            name="Otto Carmen",
            description="You are a calm concierge at a car dealership.",
        )

        await agent.create_guideline(
            condition="the customer greets you",
            action="offer a refreshing drink and ask how you can help",
        )

        print("Agent ready at http://localhost:8800. Open the Parlant UI and greet the agent, then press Enter to exit.")
        await asyncio.to_thread(input)


if __name__ == "__main__":
    asyncio.run(main())
