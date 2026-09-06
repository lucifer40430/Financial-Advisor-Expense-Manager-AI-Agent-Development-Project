from backend.database.financial_analysis import get_financial_summary


def calculate_financial_health(user_id):

    summary = get_financial_summary(user_id)

    savings_rate = summary.get("savings_rate", 0)
    expense_ratio = summary.get("expense_ratio", 0)
    debt_to_income = summary.get("debt_to_income", 0)
    budget_utilization = summary.get("budget_utilization", 0)

    # Make sure values are numbers
    savings_rate = float(savings_rate or 0)
    expense_ratio = float(expense_ratio or 0)
    debt_to_income = float(debt_to_income or 0)
    budget_utilization = float(budget_utilization or 0)

    # ==================================================
    # SAVINGS SCORE - 25 POINTS
    # ==================================================

    if savings_rate >= 30:
        savings_score = 25
    elif savings_rate >= 20:
        savings_score = 20
    elif savings_rate >= 10:
        savings_score = 15
    elif savings_rate > 0:
        savings_score = 8
    else:
        savings_score = 0

    # ==================================================
    # EXPENSE SCORE - 25 POINTS
    # ==================================================

    if expense_ratio <= 50:
        expense_score = 25
    elif expense_ratio <= 60:
        expense_score = 20
    elif expense_ratio <= 70:
        expense_score = 15
    elif expense_ratio <= 80:
        expense_score = 8
    else:
        expense_score = 0

    # ==================================================
    # DEBT SCORE - 20 POINTS
    # ==================================================

    if debt_to_income <= 20:
        debt_score = 20
    elif debt_to_income <= 30:
        debt_score = 16
    elif debt_to_income <= 40:
        debt_score = 10
    elif debt_to_income <= 50:
        debt_score = 5
    else:
        debt_score = 0

    # ==================================================
    # BUDGET SCORE - 30 POINTS
    # ==================================================

    if budget_utilization <= 70:
        budget_score = 30
    elif budget_utilization <= 80:
        budget_score = 25
    elif budget_utilization <= 90:
        budget_score = 15
    elif budget_utilization <= 100:
        budget_score = 8
    else:
        budget_score = 0

    # ==================================================
    # FINAL SCORE
    # ==================================================

    score = (
        savings_score
        + expense_score
        + debt_score
        + budget_score
    )

    # ==================================================
    # HEALTH CATEGORY
    # ==================================================

    if score >= 80:
        status = "Excellent"
        emoji = "🟢"

    elif score >= 65:
        status = "Healthy"
        emoji = "🟢"

    elif score >= 50:
        status = "Moderate"
        emoji = "🟡"

    elif score >= 35:
        status = "Needs Attention"
        emoji = "🟠"

    else:
        status = "Critical"
        emoji = "🔴"

    return {
        "score": score,
        "status": status,
        "emoji": emoji,
        "savings_rate": savings_rate,
        "expense_ratio": expense_ratio,
        "debt_to_income": debt_to_income,
        "budget_utilization": budget_utilization,
        "savings_score": savings_score,
        "expense_score": expense_score,
        "debt_score": debt_score,
        "budget_score": budget_score
    }