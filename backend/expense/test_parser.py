from expense_parser import parse_expense


ocr_text = """
Paid ₹450 to Swiggy
Date: 26 July 2026
Payment method: UPI
Transaction successful
"""


try:

    expense = parse_expense(ocr_text)

    print("\n========== EXPENSE DATA ==========\n")

    print(expense)

    print("\n==================================\n")

except Exception as e:

    print("Parser Error:", e)