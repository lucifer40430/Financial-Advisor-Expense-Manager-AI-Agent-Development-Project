from pathlib import Path

from backend.ocr.vision_ocr import vision_transcribe
from backend.expense.expense_parser import parse_expense
from backend.database.expense_db import save_expense


PROJECT_ROOT = Path(__file__).resolve().parents[2]

IMAGE_PATH = PROJECT_ROOT / "payment.png"

USER_ID = 1


def process_expense():

    if not IMAGE_PATH.exists():
        print("❌ payment.png not found")
        print("Expected:", IMAGE_PATH)
        return

    try:

        # 1. OCR
        print("\n[1/3] Reading payment screenshot...")

        ocr_text = vision_transcribe(IMAGE_PATH)

        print("\nOCR TEXT:")
        print(ocr_text)


        # 2. OCR → JSON
        print("\n[2/3] Extracting expense information...")

        expense = parse_expense(ocr_text)

        print("\nEXPENSE DATA:")

        for key, value in expense.items():
            print(f"{key}: {value}")


        # 3. JSON → MySQL
        print("\n[3/3] Saving to MySQL...")

        expense_id = save_expense(
            expense=expense,
            user_id=USER_ID,
            image_path=str(IMAGE_PATH)
        )

        print("\n✅ EXPENSE SAVED SUCCESSFULLY")
        print("Expense ID:", expense_id)


    except Exception as e:

        print("\n❌ ERROR:")
        print(type(e).__name__)
        print(e)


if __name__ == "__main__":
    process_expense()