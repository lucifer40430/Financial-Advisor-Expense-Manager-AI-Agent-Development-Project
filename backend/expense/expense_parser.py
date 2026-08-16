import json
from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="gemma4:cloud",
    temperature=0
)


def parse_expense(ocr_text: str) -> dict:

    prompt = f"""
You are an expense data extraction system.

Extract financial transaction information from the OCR text below.

Return ONLY valid JSON.

Required fields:

- amount: number
- merchant: string
- category: string
- payment_method: string
- expense_date: string in YYYY-MM-DD format

Allowed categories:

Food
Transport
Shopping
Bills
Entertainment
Education
Healthcare
Other

If a field cannot be identified, use null.

OCR TEXT:
{ocr_text}

Return JSON only.
"""

    response = llm.invoke(prompt)

    content = response.content.strip()

    # Remove markdown code fences if model adds them
    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    try:
        expense = json.loads(content)

    except json.JSONDecodeError:
        raise ValueError(
            f"LLM did not return valid JSON:\n{content}"
        )

    return expense