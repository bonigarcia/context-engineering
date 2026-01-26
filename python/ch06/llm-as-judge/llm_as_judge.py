import os
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- 1. Build a simple RAG pipeline ---

# Documents for the knowledge base
documents = [
    "The capital of France is Paris, a major European city and a global center for art, fashion, and culture.",
    "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris.",
    "The official language of France is French.",
]

# Create a FAISS vector store
embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
vectorstore = FAISS.from_texts(documents, embedding=embeddings)
retriever = vectorstore.as_retriever()

# Define the LLM and the prompt template
llm = ChatOpenAI(model_name="gpt-4o", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = PromptTemplate.from_template(template)

# Create the RAG chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- 2. Create an evaluation dataset ---

# This dataset contains questions, the expected answers, and the context (which Ragas will use to evaluate retrieval)
eval_dataset = Dataset.from_dict(
    {
        "question": [
            "What is the capital of France?",
            "What is the Eiffel Tower made of?",
            "What is the official language of Italy?", # A question with no context
        ],
        "ground_truth": [
            "The capital of France is Paris.",
            "The Eiffel Tower is made of wrought-iron.",
            "The provided context does not mention the official language of Italy.",
        ],
        "contexts": [
            ["The capital of France is Paris..."],
            ["The Eiffel Tower is a wrought-iron lattice tower..."],
            [], # No context is expected to be retrieved
        ],
    }
)

# Generate responses and add them to the dataset
responses = rag_chain.batch(eval_dataset["question"])
eval_dataset = eval_dataset.add_column("response", responses)


# --- 3. Run the evaluation with Ragas ---

print("--- Evaluating RAG pipeline with Ragas (LLM-as-Judge) ---")

# Define the metrics for evaluation
metrics = [
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
]

# Run the evaluation
result = evaluate(
    dataset=eval_dataset,
    metrics=metrics,
    llm=llm,
    embeddings=embeddings,
    raise_exceptions=False, # Set to False to see all results even if some fail
)

print("\n--- Evaluation Results ---")
print(result)

# Convert to a pandas DataFrame for better visualization
df = result.to_pandas()
print("\n--- Evaluation Results (DataFrame) ---")
print(df)


# --- 4. Demonstrate how to create a .env file ---
if not os.path.exists(".env"):
    with open(".env", "w") as f:
        f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
    print("\n--- .env file created ---")
    print("Please edit the .env file and and your OpenAI API key.")

