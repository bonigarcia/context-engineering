import os
from dotenv import load_dotenv
from datasets import Dataset

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from ragas import evaluate

from ragas.metrics._faithfulness import faithfulness
from ragas.metrics._answer_relevance import answer_relevancy
from ragas.metrics._context_recall import context_recall
from ragas.metrics._context_precision import context_precision


def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set (env var or .env).")

    # --- 1) Build a simple RAG pipeline (LangChain) ---
    documents = [
        "The capital of France is Paris, a major European city and a global center for art, fashion, and culture.",
        "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris.",
        "The official language of France is French.",
    ]

    # Vector store
    embeddings = OpenAIEmbeddings(api_key=api_key)
    vectorstore = FAISS.from_texts(documents, embedding=embeddings)
    retriever = vectorstore.as_retriever()

    # LLM used for generating answers
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0, api_key=api_key)

    template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
    prompt = PromptTemplate.from_template(template)

    rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    # --- 2) Create evaluation dataset ---
    eval_dataset = Dataset.from_dict(
        {
            "question": [
                "What is the capital of France?",
                "What is the Eiffel Tower made of?",
                "What is the official language of Italy?",  # no supporting context
            ],
            "ground_truth": [
                "The capital of France is Paris.",
                "The Eiffel Tower is made of wrought-iron.",
                "The provided context does not mention the official language of Italy.",
            ],
            # NOTE: This is a toy dataset; in a real evaluation you’d store retrieved
            # contexts per question. Keeping your original structure.
            "contexts": [
                ["The capital of France is Paris..."],
                ["The Eiffel Tower is a wrought-iron lattice tower..."],
                [],
            ],
        }
    )

    # Generate responses
    responses = rag_chain.batch(eval_dataset["question"])
    eval_dataset = eval_dataset.add_column("response", responses)

    # --- 3) Evaluate with Ragas (LLM-as-Judge) ---
    print("--- Evaluating RAG pipeline with Ragas (LLM-as-Judge) ---")

    metrics = [
        faithfulness,
        answer_relevancy,
        context_recall,
        context_precision,
    ]

    # Pass your LangChain llm/embeddings; Ragas will wrap them internally.
    result = evaluate(
        dataset=eval_dataset,
        metrics=metrics,
        llm=llm,
        embeddings=embeddings,
        raise_exceptions=False,
    )

    print("\n--- Evaluation Results ---")
    print(result)

    df = result.to_pandas()
    print("\n--- Evaluation Results (DataFrame) ---")
    print(df)


if __name__ == "__main__":
    main()
