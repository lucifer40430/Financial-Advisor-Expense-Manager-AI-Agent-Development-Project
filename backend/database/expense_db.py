from .db import get_connection


def save_expense(expense, user_id, image_path=None):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO expenses (
                user_id,
                amount,
                merchant_name,
                category,
                payment_method,
                expense_date,
                image_path
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            user_id,
            expense.get("amount"),
            expense.get("merchant"),
            expense.get("category"),
            expense.get("payment_method"),
            expense.get("expense_date"),
            image_path
        )

        cursor.execute(query, values)
        connection.commit()

        return cursor.lastrowid

    except Exception:
        if connection:
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()