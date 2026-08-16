from pathlib import Path

from backend.ocr.vision_ocr import vision_transcribe
from backend.expense.expense_parser import parse_expense
from backend.database.expense_db import save_expense


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

IMAGE_PATH = PROJECT_ROOT / "payment.png"

USER_ID = 1


# ============================================================
# PROCESS EXPENSE
# ============================================================

def process_expense():

    # --------------------------------------------------------
    # Check image
    # --------------------------------------------------------

    if not IMAGE_PATH.exists():
        print("❌ Payment image not found!")
        print(f"Expected location: {IMAGE_PATH}")
        return


    try:

        # ====================================================
        # STEP 1: OCR
        # ====================================================

        print("\n[1/3] Reading payment screenshot...")

        ocr_text = vision_transcribe(IMAGE_PATH)

        print("\n========== OCR TEXT ==========")
        print(ocr_text)
        print("===============================")


        # ====================================================
        # STEP 2: OCR → STRUCTURED EXPENSE
        # ====================================================

        print("\n[2/3] Extracting expense information...")

        expense = parse_expense(ocr_text)

        print("\n====== STRUCTURED EXPENSE ======")

        for key, value in expense.items():
            print(f"{key}: {value}")

        print("================================")


        # ====================================================
        # STEP 3: SAVE TO MYSQL
        # ====================================================

        print("\n[3/3] Saving expense to MySQL...")

        expense_id = save_expense(
            expense=expense,
            user_id=USER_ID,
            image_path=str(IMAGE_PATH)
        )


        # ====================================================
        # SUCCESS
        # ====================================================

        print("\n========================================")
        print("     ✅ EXPENSE SAVED SUCCESSFULLY")
        print("========================================")

        print(f"Expense ID : {expense_id}")
        print(f"Amount     : {expense.get('amount')}")
        print(f"Merchant   : {expense.get('merchant')}")
        print(f"Category   : {expense.get('category')}")
        print(f"Payment    : {expense.get('payment_method')}")
        print(f"Date       : {expense.get('expense_date')}")

        print("========================================")


    except Exception as e:

        print("\n========================================")
        print("          ❌ PIPELINE ERROR")
        print("========================================")

        print(type(e).__name__)
        print(e)

        print("========================================")


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    process_expense()