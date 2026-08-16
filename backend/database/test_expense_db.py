from expense_db import save_expense


test_expense = {
    "amount": 450.00,
    "merchant": "Swiggy",
    "category": "Food",
    "payment_method": "UPI",
    "expense_date": "2026-07-26"
}


try:

    expense_id = save_expense(
        expense=test_expense,
        user_id=1,
        image_path="uploads/payment.png"
    )

    print("✅ Expense saved successfully")
    print("Expense ID:", expense_id)

except Exception as e:

    print("❌ Error:", e)