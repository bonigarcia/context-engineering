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
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.evaluation import (
    AnswerRelevancyEvaluator,
    ContextRelevancyEvaluator,
)
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Check if OPENAI_API_KEY is set
if os.getenv("OPENAI_API_KEY") is None:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# 1. Define dummy data and a simple RAG pipeline
documents = SimpleDirectoryReader(input_files=["data.txt"]).load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(llm=OpenAI(model="gpt-5-mini"))

# 2. Define a small, pre-defined dataset for evaluation
# In a real scenario, you would use RagDatasetGenerator for synthetic data or a manually curated dataset.
eval_questions = [
    "What is LlamaIndex?",
    "What is the capital of France?",
    "Where is the Eiffel Tower located?",
]

# For each question, we'll get the prediction from our RAG pipeline
predictions = []
for question in eval_questions:
    response = query_engine.query(question)
    predictions.append({
        "query": question,
        "response": str(response),
        "contexts": [n.get_content() for n in response.source_nodes]
    })

# 3. Initialize evaluators
llm = OpenAI(model="gpt-5-mini")
embed_model = OpenAIEmbedding(model="text-embedding-ada-002")

answer_relevancy_evaluator = AnswerRelevancyEvaluator(llm=llm)
context_relevancy_evaluator = ContextRelevancyEvaluator(llm=llm, embed_model=embed_model)

# 4. Perform evaluation
answer_relevancy_results = []
context_relevancy_results = []

print("Running evaluations...")
for pred in predictions:
    # Evaluate answer relevancy
    eval_ar = answer_relevancy_evaluator.evaluate(
        query=pred["query"],
        response=pred["response"],
    )
    answer_relevancy_results.append(eval_ar)

    # Evaluate context relevancy
    eval_cr = context_relevancy_evaluator.evaluate(
        query=pred["query"],
        contexts=pred["contexts"],
    )
    context_relevancy_results.append(eval_cr)

# 5. Print evaluation results
print("--- Answer Relevancy Results ---")
ar_df = pd.DataFrame([{"query": res.query, "score": res.score, "feedback": res.feedback} for res in answer_relevancy_results])
print(ar_df)

print("--- Context Relevancy Results ---")
cr_df = pd.DataFrame([{"query": res.query, "score": res.score, "feedback": res.feedback} for res in context_relevancy_results])
print(cr_df)

# Clean up the dummy data file
os.remove("data.txt")
