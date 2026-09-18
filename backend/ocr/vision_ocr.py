import os
import base64
import mimetypes
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# OCR PROMPT
# ============================================================

TRANSCRIBE_PROMPT = """
You are an OCR system for financial payment screenshots.

Extract all visible text from the image.

Rules:
1. Transcribe the text as accurately as possible.
2. Do NOT invent information.
3. Preserve numbers exactly.
4. Include:
   - Merchant name
   - Transaction amount
   - Date
   - Time
   - Transaction ID / UTR
   - Payment method
   - Bank / UPI information
   - Any other visible transaction information
5. If a piece of text is unclear, write your best reading.
6. Do not analyze the transaction.
7. Do not explain anything.
8. Output ONLY the text visible in the image.
"""


# ============================================================
# GET OLLAMA API KEY
# ============================================================

def get_ollama_api_key():
    """
    Get Ollama API key.

    Priority:
    1. Streamlit Secrets - deployed app
    2. .env / environment variable - local development
    """

    # --------------------------------------------------------
    # 1. Streamlit Cloud Secrets
    # --------------------------------------------------------

    try:
        api_key = st.secrets.get("ollama_api_key")

        if api_key:
            return str(api_key).strip()

    except Exception:
        pass

    # --------------------------------------------------------
    # 2. Local .env
    # --------------------------------------------------------

    api_key = os.getenv("ollama_api_key")

    if api_key:
        return api_key.strip()

    # --------------------------------------------------------
    # 3. Optional uppercase fallback
    # --------------------------------------------------------

    api_key = os.getenv("OLLAMA_API_KEY")

    if api_key:
        return api_key.strip()

    # --------------------------------------------------------
    # Nothing found
    # --------------------------------------------------------

    raise RuntimeError(
        "Ollama API key not found. "
        "Add 'ollama_api_key' to Streamlit Secrets "
        "or your local .env file."
    )


# ============================================================
# INITIALIZE OLLAMA
# ============================================================

OLLAMA_API_KEY = get_ollama_api_key()


llm = ChatOllama(
    model="gemma4:cloud",
    temperature=0,
    base_url="https://ollama.com",
    client_kwargs={
        "headers": {
            "Authorization": f"Bearer {OLLAMA_API_KEY}"
        }
    },
)


# ============================================================
# VISION OCR FUNCTION
# ============================================================

def vision_transcribe(image_path: Path) -> str:
    """
    Extract visible text from an image using Ollama Cloud.
    """

    # --------------------------------------------------------
    # Validate image
    # --------------------------------------------------------

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    if not image_path.is_file():
        raise ValueError(
            f"Invalid image path: {image_path}"
        )

    # --------------------------------------------------------
    # Detect MIME type
    # --------------------------------------------------------

    mime_type, _ = mimetypes.guess_type(
        str(image_path)
    )

    if mime_type is None:
        mime_type = "image/png"

    # --------------------------------------------------------
    # Read image
    # --------------------------------------------------------

    image_bytes = image_path.read_bytes()

    if not image_bytes:
        raise ValueError(
            "The uploaded image is empty."
        )

    # --------------------------------------------------------
    # Convert image to Base64
    # --------------------------------------------------------

    encoded_image = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    # --------------------------------------------------------
    # Create multimodal message
    # --------------------------------------------------------

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": TRANSCRIBE_PROMPT,
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": (
                        f"data:{mime_type};base64,"
                        f"{encoded_image}"
                    )
                },
            },
        ]
    )

    # --------------------------------------------------------
    # Send image to Ollama Cloud
    # --------------------------------------------------------

    try:

        response = llm.invoke([message])

    except Exception as e:

        error_message = str(e)

        if "401" in error_message:
            raise RuntimeError(
                "Ollama Cloud authentication failed (401). "
                "Check that your Ollama API key is valid "
                "and correctly configured in Streamlit Secrets."
            ) from e

        raise RuntimeError(
            f"Ollama OCR request failed: {error_message}"
        ) from e

    # --------------------------------------------------------
    # Extract response
    # --------------------------------------------------------

    if not response or not response.content:
        raise RuntimeError(
            "Ollama returned an empty OCR response."
        )

    return response.content.strip()