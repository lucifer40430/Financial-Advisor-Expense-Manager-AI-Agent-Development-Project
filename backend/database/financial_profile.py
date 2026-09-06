from .db import get_connection


def save_profile(
    user_id,
    monthly_income,
    current_savings,
    fixed_monthly_expenses,
    monthly_debt_payment,
    financial_goal,
    goal_amount,
    goal_deadline,
    risk_preference
):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO financial_profiles (
                user_id,
                monthly_income,
                current_savings,
                fixed_monthly_expenses,
                monthly_debt_payment,
                financial_goal,
                goal_amount,
                goal_deadline,
                risk_preference
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                monthly_income = VALUES(monthly_income),
                current_savings = VALUES(current_savings),
                fixed_monthly_expenses = VALUES(fixed_monthly_expenses),
                monthly_debt_payment = VALUES(monthly_debt_payment),
                financial_goal = VALUES(financial_goal),
                goal_amount = VALUES(goal_amount),
                goal_deadline = VALUES(goal_deadline),
                risk_preference = VALUES(risk_preference)
        """

        values = (
            user_id,
            monthly_income,
            current_savings,
            fixed_monthly_expenses,
            monthly_debt_payment,
            financial_goal,
            goal_amount,
            goal_deadline,
            risk_preference
        )

        cursor.execute(query, values)
        connection.commit()

    except Exception:
        if connection:
            connection.rollback()
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def get_profile(user_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                profile_id,
                user_id,
                monthly_income,
                current_savings,
                fixed_monthly_expenses,
                monthly_debt_payment,
                financial_goal,
                goal_amount,
                goal_deadline,
                risk_preference
            FROM financial_profiles
            WHERE user_id = %s
        """

        cursor.execute(query, (user_id,))

        return cursor.fetchone()

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()