import base64
import mimetypes
from pathlib import Path

from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI


# Load the nearest .env file (searches parent directories)
load_dotenv(find_dotenv())


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


def vision_transcribe(image_path: Path) -> str:
    """
    Extract visible text from an image using a vision-capable LLM.
    """

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    # Detect image MIME type
    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type is None:
        mime_type = "image/png"

    # Read image
    image_bytes = image_path.read_bytes()

    # Convert image to Base64
    b64_image = base64.b64encode(image_bytes).decode("utf-8")

    # Create Vision LLM
    llm = ChatOpenAI(
        model="gpt-4.1-nano",
        temperature=0
    )

    # Multimodal message
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

    # Send image + prompt
    response = llm.invoke([message])

    return response.content.strip()