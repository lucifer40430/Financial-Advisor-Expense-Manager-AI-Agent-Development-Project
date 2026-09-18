import os
import base64
import mimetypes
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

load_dotenv()


TRANSCRIBE_PROMPT = """
Transcribe all visible text in this image exactly as written.

Rules:
- Preserve the original text as closely as possible.
- Do not invent missing information.
- Include numbers, dates, merchant names, transaction IDs,
  payment methods, and amounts.
- If some text is unclear, make your best reading.
- Output only the transcribed text.
"""


# --------------------------------------------------
# Get Ollama API Key
# --------------------------------------------------

OLLAMA_API_KEY = os.getenv("ollama_api_key")

# When deployed on Streamlit Cloud, read from Secrets
if not OLLAMA_API_KEY:
    try:
        OLLAMA_API_KEY = st.secrets["ollama_api_key"]
    except Exception:
        OLLAMA_API_KEY = None


if not OLLAMA_API_KEY:
    raise RuntimeError(
        "Ollama API key not configured. "
        "Add ollama_api_key to .env or Streamlit Secrets."
    )


# --------------------------------------------------
# Ollama Cloud
# --------------------------------------------------

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


# --------------------------------------------------
# Vision OCR
# --------------------------------------------------

def vision_transcribe(image_path: Path) -> str:
    """
    Extract visible text from an image using Ollama Cloud.
    """

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    # Detect image MIME type
    mime_type, _ = mimetypes.guess_type(str(image_path))

    if mime_type is None:
        mime_type = "image/png"

    # Read image
    image_bytes = image_path.read_bytes()

    # Convert image to Base64
    b64_image = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    # Create multimodal message
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": TRANSCRIBE_PROMPT,
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{b64_image}"
                },
            },
        ]
    )

    # Send image to Ollama Cloud
    response = llm.invoke([message])

    return response.content.strip()