from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# ============================================================
# 1. PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHROMA_PATH = PROJECT_ROOT / "data" / "chroma_db"


# ============================================================
# 2. EMBEDDING MODEL
# ============================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ============================================================
# 3. LOAD CHROMA DATABASE
# ============================================================

vectorstore = Chroma(
    persist_directory=str(CHROMA_PATH),
    embedding_function=embeddings
)


# ============================================================
# 4. RETRIEVE RELEVANT FINANCIAL KNOWLEDGE
# ============================================================

def retrieve_financial_context(
    question,
    k=4,
    max_distance=1.10
):
    """
    Retrieve relevant financial knowledge from ChromaDB.

    Lower distance = more relevant result.
    """

    if not question or not question.strip():
        return "No financial question was provided."

    try:

        # Retrieve extra candidates first
        results = vectorstore.similarity_search_with_score(
            question,
            k=8
        )

        if not results:
            return "No relevant financial knowledge found."

        # ----------------------------------------------------
        # Filter weak results
        # ----------------------------------------------------

        relevant_results = []

        for document, score in results:

            if score <= max_distance:
                relevant_results.append(
                    (document, score)
                )

        if not relevant_results:
            return (
                "No sufficiently relevant financial knowledge "
                "was found for this question."
            )

        # ----------------------------------------------------
        # Remove duplicate content
        # ----------------------------------------------------

        unique_results = []
        seen_content = set()

        for document, score in relevant_results:

            content = document.page_content.strip()

            if content in seen_content:
                continue

            seen_content.add(content)

            unique_results.append(
                (document, score)
            )

        # Keep only the best results
        unique_results = unique_results[:k]

        # ----------------------------------------------------
        # Build structured context
        # ----------------------------------------------------

        context_parts = []

        for index, (document, score) in enumerate(
            unique_results,
            start=1
        ):

            source = document.metadata.get(
                "source",
                "Unknown"
            )

            page = document.metadata.get(
                "page",
                "Unknown"
            )

            chunk_id = document.metadata.get(
                "chunk_id",
                "Unknown"
            )

            document_type = document.metadata.get(
                "document_type",
                "Unknown"
            )

            context_parts.append(
                f"""
--- FINANCIAL SOURCE {index} ---

Source: {source}
Page: {page}
Chunk: {chunk_id}
Document Type: {document_type}
Relevance Distance: {score:.4f}

Content:
{document.page_content}

--- END SOURCE {index} ---
"""
            )

        return "\n".join(context_parts)

    except Exception as e:

        return (
            "Financial knowledge retrieval failed. "
            f"Error: {type(e).__name__}: {e}"
        )