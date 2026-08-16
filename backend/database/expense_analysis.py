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