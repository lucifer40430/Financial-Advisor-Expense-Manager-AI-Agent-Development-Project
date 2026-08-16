from pathlib import Path

import fitz  # PyMuPDF

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# ============================================================
# 1. PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PDF_PATH = PROJECT_ROOT / "data" / "documents" / "financial_book.pdf"

CHROMA_PATH = PROJECT_ROOT / "data" / "chroma_db"


# ============================================================
# 2. CHECK PDF
# ============================================================

if not PDF_PATH.exists():
    raise FileNotFoundError(
        f"\nPDF not found:\n{PDF_PATH}\n"
    )

print("PDF found:")
print(PDF_PATH)


# ============================================================
# 3. READ PDF USING PYMUPDF
# ============================================================

print("\nLoading PDF...")

pdf = fitz.open(str(PDF_PATH))

documents = []

for page_number, page in enumerate(pdf):

    text = page.get_text()

    if text.strip():

        documents.append({
            "text": text,
            "page": page_number + 1
        })

pdf.close()

print(f"PDF loaded successfully.")
print(f"Pages with text: {len(documents)}")


# ============================================================
# 4. SPLIT TEXT INTO CHUNKS
# ============================================================

print("\nSplitting document into chunks...")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

chunks = []

for document in documents:

    split_texts = text_splitter.split_text(
        document["text"]
    )

    for text in split_texts:

        chunks.append({
            "text": text,
            "page": document["page"]
        })


print(f"Created {len(chunks)} chunks.")


# ============================================================
# 5. CREATE LANGCHAIN DOCUMENTS
# ============================================================

from langchain_core.documents import Document

langchain_documents = []

for chunk in chunks:

    langchain_documents.append(
        Document(
            page_content=chunk["text"],
            metadata={
                "source": PDF_PATH.name,
                "page": chunk["page"]
            }
        )
    )


# ============================================================
# 6. CREATE EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded.")


# ============================================================
# 7. CREATE CHROMA VECTOR DATABASE
# ============================================================

print("\nCreating ChromaDB...")

Chroma.from_documents(
    documents=langchain_documents,
    embedding=embeddings,
    persist_directory=str(CHROMA_PATH)
)


# ============================================================
# 8. FINISHED
# ============================================================

print("\n======================================")
print("RAG INGESTION COMPLETED SUCCESSFULLY")
print("======================================")

print(f"Pages processed : {len(documents)}")
print(f"Chunks created  : {len(chunks)}")
print(f"Vector database : {CHROMA_PATH}")