from datetime import date

from backend.database.financial_profile import get_profile
from backend.database.financial_analysis import get_financial_summary


def calculate_goal_progress(user_id):

    profile = get_profile(user_id)

    if not profile:
        return None

    goal_amount = float(profile.get("goal_amount") or 0)
    current_savings = float(profile.get("current_savings") or 0)
    goal_deadline = profile.get("goal_deadline")

    # No valid goal configured
    if goal_amount <= 0 or not goal_deadline:
        return None

    # --------------------------------------------------
    # BASIC CALCULATIONS
    # --------------------------------------------------

    remaining_amount = max(
        goal_amount - current_savings,
        0
    )

    progress_percentage = min(
        (current_savings / goal_amount) * 100,
        100
    )

    # --------------------------------------------------
    # MONTHS REMAINING
    # --------------------------------------------------

    today = date.today()

    months_remaining = (
        (goal_deadline.year - today.year) * 12
        + (goal_deadline.month - today.month)
    )

    # If deadline is in the current month,
    # consider at least one month available.
    months_remaining = max(months_remaining, 1)

    # --------------------------------------------------
    # REQUIRED MONTHLY SAVING
    # --------------------------------------------------

    required_monthly_saving = (
        remaining_amount / months_remaining
    )

    # --------------------------------------------------
    # CURRENT SAVING CAPACITY
    # --------------------------------------------------

    summary = get_financial_summary(user_id)

    monthly_surplus = float(
        summary.get("monthly_surplus") or 0
    )

    # --------------------------------------------------
    # GOAL STATUS
    # --------------------------------------------------

    if remaining_amount <= 0:

        status = "Achieved"
        emoji = "🏆"

    elif monthly_surplus >= required_monthly_saving:

        status = "On Track"
        emoji = "🟢"

    elif monthly_surplus > 0:

        status = "At Risk"
        emoji = "🟡"

    else:

        status = "Unlikely"
        emoji = "🔴"

    return {
        "goal": profile.get("financial_goal"),
        "goal_amount": goal_amount,
        "current_savings": current_savings,
        "remaining_amount": remaining_amount,
        "progress_percentage": progress_percentage,
        "goal_deadline": goal_deadline,
        "months_remaining": months_remaining,
        "required_monthly_saving": required_monthly_saving,
        "monthly_surplus": monthly_surplus,
        "status": status,
        "emoji": emoji
    }