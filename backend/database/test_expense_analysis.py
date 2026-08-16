from .expense_analysis import get_user_expenses


USER_ID = 1


try:

    expenses = get_user_expenses(USER_ID)

    print("\n========== USER EXPENSES ==========\n")

    if not expenses:
        print("No expenses found.")

    else:
        for expense in expenses:
            print(
                f"{expense['expense_date']} | "
                f"{expense['merchant_name']} | "
                f"₹{expense['amount']} | "
                f"{expense['category']} | "
                f"{expense['payment_method']}"
            )

    print("\n===================================\n")


except Exception as e:

    print("❌ Error:", e)