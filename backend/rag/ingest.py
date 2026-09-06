import shutil
from pathlib import Path

import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parents[2]

DOCUMENTS_DIR = BASE_DIR / "data" / "documents"
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"


# =========================
# SETTINGS
# =========================

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# =========================
# LOAD ALL PDFS
# =========================

pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

if not pdf_files:
    raise FileNotFoundError(
        f"No PDF files found in: {DOCUMENTS_DIR}"
    )

print("\n========== DOCUMENTS ==========")

for pdf in pdf_files:
    print(f"Found: {pdf.name}")

print("================================\n")


# =========================
# TEXT SPLITTER
# =========================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)


all_documents = []


# =========================
# PROCESS EACH PDF
# =========================

for pdf_path in pdf_files:

    print(f"\nProcessing: {pdf_path.name}")

    document_id = pdf_path.stem

    pdf = fitz.open(pdf_path)

    document_chunk_count = 0

    for page_number, page in enumerate(pdf, start=1):

        text = page.get_text("text").strip()

        if not text:
            continue

        chunks = text_splitter.split_text(text)

        for chunk_index, chunk in enumerate(chunks):

            metadata = {
                "source": pdf_path.name,
                "document_id": document_id,
                "page": page_number,
                "chunk_id": document_chunk_count,
                "document_type": "financial_education",
                "publisher": "SEBI",
                "jurisdiction": "India"
            }

            all_documents.append(
                {
                    "page_content": chunk,
                    "metadata": metadata
                }
            )

            document_chunk_count += 1

    pdf.close()

    print(
        f"Created {document_chunk_count} chunks "
        f"from {pdf_path.name}"
    )


# =========================
# CONVERT TO LANGCHAIN DOCUMENTS
# =========================

from langchain_core.documents import Document

documents = [
    Document(
        page_content=item["page_content"],
        metadata=item["metadata"]
    )
    for item in all_documents
]


# =========================
# DELETE OLD CHROMA DATABASE
# =========================

if CHROMA_DIR.exists():

    print("\nDeleting old Chroma database...")

    shutil.rmtree(CHROMA_DIR)


# =========================
# EMBEDDINGS
# =========================

print("\nLoading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)


# =========================
# CREATE CHROMA DATABASE
# =========================

print("\nCreating Chroma database...")

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory=str(CHROMA_DIR)
)


print("\n================================")
print("RAG INGESTION COMPLETED")
print("================================")
print(f"PDF files: {len(pdf_files)}")
print(f"Total chunks: {len(documents)}")
print(f"Chroma path: {CHROMA_DIR}")