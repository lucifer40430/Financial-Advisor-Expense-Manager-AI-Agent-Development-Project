import base64
import mimetypes
from pathlib import Path

from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama


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


# Ollama Cloud model
llm = ChatOllama(
    model="gemma4:cloud",
    temperature=0
)


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

    # Send image + prompt to Ollama Cloud
    response = llm.invoke([message])

    return response.content.strip()