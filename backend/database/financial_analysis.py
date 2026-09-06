from .db import get_connection


def get_financial_summary(user_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # ============================================================
        # CURRENT MONTH
        # ============================================================

        # ------------------------------------------------------------
        # Monthly income
        # ------------------------------------------------------------

        cursor.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS monthly_income
            FROM income
            WHERE user_id = %s
            AND MONTH(income_date) = MONTH(CURDATE())
            AND YEAR(income_date) = YEAR(CURDATE())
            """,
            (user_id,)
        )

        income_result = cursor.fetchone()
        monthly_income = float(income_result["monthly_income"] or 0)

        # ------------------------------------------------------------
        # Monthly expenses
        # ------------------------------------------------------------

        cursor.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS monthly_expenses
            FROM expenses
            WHERE user_id = %s
            AND MONTH(expense_date) = MONTH(CURDATE())
            AND YEAR(expense_date) = YEAR(CURDATE())
            """,
            (user_id,)
        )

        expense_result = cursor.fetchone()
        monthly_expenses = float(expense_result["monthly_expenses"] or 0)

        # ------------------------------------------------------------
        # Monthly surplus
        # ------------------------------------------------------------

        monthly_surplus = monthly_income - monthly_expenses

        # ------------------------------------------------------------
        # Savings rate
        # ------------------------------------------------------------

        if monthly_income > 0:
            savings_rate = (
                monthly_surplus / monthly_income
            ) * 100
        else:
            savings_rate = 0

        # ------------------------------------------------------------
        # Expense ratio
        # ------------------------------------------------------------

        if monthly_income > 0:
            expense_ratio = (
                monthly_expenses / monthly_income
            ) * 100
        else:
            expense_ratio = 0

        # ------------------------------------------------------------
        # Debt / EMI
        # ------------------------------------------------------------

        cursor.execute(
            """
            SELECT monthly_debt_payment
            FROM financial_profiles
            WHERE user_id = %s
            """,
            (user_id,)
        )

        profile = cursor.fetchone()

        monthly_debt_payment = 0

        if profile:
            monthly_debt_payment = float(
                profile["monthly_debt_payment"] or 0
            )

        # ------------------------------------------------------------
        # Debt-to-income ratio
        # ------------------------------------------------------------

        if monthly_income > 0:
            debt_to_income_ratio = (
                monthly_debt_payment / monthly_income
            ) * 100
        else:
            debt_to_income_ratio = 0

        # ============================================================
        # CATEGORY-WISE SPENDING
        # ============================================================

        cursor.execute(
            """
            SELECT
                category,
                COALESCE(SUM(amount), 0) AS total
            FROM expenses
            WHERE user_id = %s
            AND MONTH(expense_date) = MONTH(CURDATE())
            AND YEAR(expense_date) = YEAR(CURDATE())
            GROUP BY category
            ORDER BY total DESC
            """,
            (user_id,)
        )

        category_spending = cursor.fetchall()

        # ============================================================
        # BUDGET VS SPENDING
        # ============================================================

        cursor.execute(
            """
            SELECT
                b.category,
                b.monthly_limit,
                COALESCE(SUM(e.amount), 0) AS spent
            FROM budget b

            LEFT JOIN expenses e
                ON b.user_id = e.user_id
                AND b.category = e.category
                AND MONTH(e.expense_date) = MONTH(CURDATE())
                AND YEAR(e.expense_date) = YEAR(CURDATE())

            WHERE b.user_id = %s

            GROUP BY
                b.category,
                b.monthly_limit

            ORDER BY b.category
            """,
            (user_id,)
        )

        budget_analysis = cursor.fetchall()

        # ------------------------------------------------------------
        # Total budget
        # ------------------------------------------------------------

        total_budget = sum(
            float(row["monthly_limit"] or 0)
            for row in budget_analysis
        )

        total_budget_spent = sum(
            float(row["spent"] or 0)
            for row in budget_analysis
        )

        # ------------------------------------------------------------
        # Budget utilization
        # ------------------------------------------------------------

        if total_budget > 0:
            budget_utilization = (
                total_budget_spent / total_budget
            ) * 100
        else:
            budget_utilization = 0

        # ============================================================
        # RETURN FINANCIAL SUMMARY
        # ============================================================

        return {
            "monthly_income": monthly_income,

            "monthly_expenses": monthly_expenses,

            "monthly_surplus": monthly_surplus,

            "savings_rate": round(savings_rate, 2),

            "expense_ratio": round(expense_ratio, 2),

            "monthly_debt_payment": monthly_debt_payment,

            "debt_to_income_ratio": round(
                debt_to_income_ratio,
                2
            ),

            "total_budget": total_budget,

            "total_budget_spent": total_budget_spent,

            "budget_utilization": round(
                budget_utilization,
                2
            ),

            "total_spending": monthly_expenses,

            "category_spending": [
                {
                    "category": row["category"],
                    "total": float(row["total"] or 0)
                }
                for row in category_spending
            ],

            "budget_analysis": [
                {
                    "category": row["category"],
                    "monthly_limit": float(
                        row["monthly_limit"] or 0
                    ),
                    "spent": float(
                        row["spent"] or 0
                    ),
                    "remaining": float(
                        row["monthly_limit"] - row["spent"]
                    )
                }
                for row in budget_analysis
            ]
        }

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()