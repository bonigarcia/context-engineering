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
import cognee


async def main():
    """
    Demonstrates basic memory operations with Cognee:
    1. Adding unstructured data (text).
    2. 'Cognifying' it (building a knowledge graph and vectorizing).
    3. Searching the memory layer with a hybrid approach.
    """
    print("=== Cognee Memory Example ===")

    # 1. Reset data for a clean start (optional)
    print("Pruning old data...")
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    # 2. Add data to memory
    print("Adding context to memory...")
    text_context = (
        "Context engineering is the process of optimizing information "
        "provided to an LLM to improve its performance and accuracy."
    )
    await cognee.add(text_context)
    print(f"Data added: '{text_context}'")

    # 3. Cognify: Process raw data into structured memory (Graph + Vector)
    print("Cognifying (building knowledge graph and vector index)...")
    await cognee.cognify()

    # 4. Search: Query the memory layer
    query = "What is context engineering?"
    print(f"Searching memory for: '{query}'")
    results = await cognee.search(query_text=query)

    print("\n--- Memory Retrieval Results ---")
    if not results:
        print("No results found.")
    else:
        for i, result in enumerate(results, 1):
            print(f"Result {i}: {result}")


if __name__ == "__main__":
    asyncio.run(main())