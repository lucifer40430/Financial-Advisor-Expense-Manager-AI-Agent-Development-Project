from backend.database.db import get_connection


def get_user_expenses(user_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                expense_id,
                amount,
                merchant_name,
                category,
                payment_method,
                expense_date
            FROM expenses
            WHERE user_id = %s
            ORDER BY expense_date DESC
        """

        cursor.execute(query, (user_id,))

        return cursor.fetchall()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# CATEGORY-WISE SPENDING
# ============================================================

def get_category_spending(user_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                category,
                COALESCE(SUM(amount), 0) AS total
            FROM expenses
            WHERE user_id = %s
            GROUP BY category
            ORDER BY total DESC
        """

        cursor.execute(query, (user_id,))

        results = cursor.fetchall()

        return [
            {
                "category": row["category"],
                "total": float(row["total"] or 0)
            }
            for row in results
        ]

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# MONTHLY SPENDING
# ============================================================

def get_monthly_spending(user_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                YEAR(expense_date) AS year,
                MONTH(expense_date) AS month,
                COALESCE(SUM(amount), 0) AS total
            FROM expenses
            WHERE user_id = %s
            GROUP BY
                YEAR(expense_date),
                MONTH(expense_date)
            ORDER BY
                year DESC,
                month DESC
        """

        cursor.execute(query, (user_id,))

        results = cursor.fetchall()

        return [
            {
                "year": row["year"],
                "month": row["month"],
                "total": float(row["total"] or 0)
            }
            for row in results
        ]

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# TOP EXPENSES
# ============================================================

def get_top_expenses(user_id, limit=5):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                expense_id,
                amount,
                merchant_name,
                category,
                payment_method,
                expense_date
            FROM expenses
            WHERE user_id = %s
            ORDER BY amount DESC
            LIMIT %s
        """

        cursor.execute(query, (user_id, limit))

        results = cursor.fetchall()

        return [
            {
                "expense_id": row["expense_id"],
                "amount": float(row["amount"] or 0),
                "merchant_name": row["merchant_name"],
                "category": row["category"],
                "payment_method": row["payment_method"],
                "expense_date": row["expense_date"]
            }
            for row in results
        ]

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ============================================================
# BUDGET OVERSPENDING
# ============================================================

def get_overspending_categories(user_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
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

            HAVING spent > b.monthly_limit

            ORDER BY
                (spent - b.monthly_limit) DESC
        """

        cursor.execute(query, (user_id,))

        results = cursor.fetchall()

        return [
            {
                "category": row["category"],
                "budget": float(row["monthly_limit"] or 0),
                "spent": float(row["spent"] or 0),
                "overspent_by": float(
                    row["spent"] - row["monthly_limit"]
                )
            }
            for row in results
        ]

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()