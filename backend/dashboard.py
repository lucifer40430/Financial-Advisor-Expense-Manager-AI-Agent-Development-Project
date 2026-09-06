import streamlit as st

from backend.database.financial_analysis import (
    get_financial_summary
)

from backend.database.expense_analysis import (
    get_category_spending,
    get_monthly_spending,
    get_top_expenses,
    get_overspending_categories
)
from backend.database.financial_health import (
    calculate_financial_health
)
from backend.database.financial_goals import (
    calculate_goal_progress
)
def show_dashboard(user_id):

    st.header("📊 Financial Dashboard")

    try:
        summary = get_financial_summary(user_id)
        category_spending = get_category_spending(user_id)
        monthly_spending = get_monthly_spending(user_id)
        top_expenses = get_top_expenses(user_id, 5)
        overspending = get_overspending_categories(user_id)
        total_spending = summary["total_spending"]
        categories = summary["category_spending"]
        budgets = summary["budget_analysis"]
        health = calculate_financial_health(user_id)
        goal = calculate_goal_progress(user_id)

        # ==================================================
        # TOP METRICS
        # ==================================================

        total_budget = sum(
            item["monthly_limit"]
            for item in budgets
        )

        total_remaining = sum(
            item["remaining"]
            for item in budgets
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "💰 Total Spending",
                f"₹{total_spending:,.2f}"
            )

        with col2:
            st.metric(
                "🎯 Total Budget",
                f"₹{total_budget:,.2f}"
            )

        with col3:
            st.metric(
                "💵 Remaining",
                f"₹{total_remaining:,.2f}"
            )
            
                # ==================================================
        # FINANCIAL HEALTH SCORE
        # ==================================================

        st.subheader("🏦 Financial Health Score")

        health_col1, health_col2 = st.columns([1, 2])

        with health_col1:

            st.metric(
                "Health Score",
                f"{health['score']} / 100"
            )

            st.write(
                f"{health['emoji']} **{health['status']}**"
            )

        with health_col2:

            st.write("### Score Breakdown")

            breakdown_col1, breakdown_col2 = st.columns(2)

            with breakdown_col1:

                st.write(
                    f"💰 **Savings:** "
                    f"{health['savings_rate']:.1f}% "
                    f"({health['savings_score']}/25)"
                )

                st.write(
                    f"💳 **Debt:** "
                    f"{health['debt_to_income']:.1f}% "
                    f"({health['debt_score']}/20)"
                )

            with breakdown_col2:

                st.write(
                    f"📊 **Expenses:** "
                    f"{health['expense_ratio']:.1f}% "
                    f"({health['expense_score']}/25)"
                )

                st.write(
                    f"🎯 **Budget Usage:** "
                    f"{health['budget_utilization']:.1f}% "
                    f"({health['budget_score']}/30)"
                )
                # ==================================================
        # FINANCIAL GOAL
        # ==================================================

        st.subheader("🎯 Financial Goal")

        if goal:

            goal_col1, goal_col2 = st.columns([1, 2])

            with goal_col1:

                st.write(
                    f"### {goal['goal']}"
                )

                st.metric(
                    "Goal Amount",
                    f"₹{goal['goal_amount']:,.2f}"
                )

                st.metric(
                    "Current Savings",
                    f"₹{goal['current_savings']:,.2f}"
                )

            with goal_col2:

                st.metric(
                    "Remaining",
                    f"₹{goal['remaining_amount']:,.2f}"
                )

                st.write(
                    f"**Progress:** "
                    f"{goal['progress_percentage']:.1f}%"
                )

                st.progress(
                    goal["progress_percentage"] / 100
                )

                st.write(
                    f"📅 **Deadline:** "
                    f"{goal['goal_deadline']}"
                )

                st.write(
                    f"⏳ **Months Remaining:** "
                    f"{goal['months_remaining']}"
                )

                st.write(
                    f"💰 **Required Monthly Saving:** "
                    f"₹{goal['required_monthly_saving']:,.2f}"
                )

                st.write(
                    f"💵 **Current Monthly Surplus:** "
                    f"₹{goal['monthly_surplus']:,.2f}"
                )

                if goal["status"] == "Achieved":

                    st.success(
                        "🏆 Goal achieved!"
                    )

                elif goal["status"] == "On Track":

                    st.success(
                        "🟢 You are on track to achieve this goal."
                    )

                elif goal["status"] == "At Risk":

                    st.warning(
                        "🟡 Your current saving rate may not "
                        "be enough to reach this goal on time."
                    )

                else:

                    st.error(
                        "🔴 Your current monthly surplus is "
                        "not sufficient to reach this goal."
                    )

        else:

            st.info(
                "No financial goal has been configured yet. "
                "Set one in your Financial Profile."
            )            
        st.divider()

        # ==================================================
        # CATEGORY SPENDING
        # ==================================================

        st.subheader("📂 Category-wise Spending")

        if categories:

            cols = st.columns(
                min(len(categories), 4)
            )

            for index, item in enumerate(categories):

                with cols[index % len(cols)]:

                    st.metric(
                        item["category"],
                        f"₹{item['total']:,.2f}"
                    )

        else:

            st.info("No expense data available.")

        st.divider()

        # ==================================================
        # BUDGET ANALYSIS
        # ==================================================

        st.subheader("💳 Budget Analysis")

        if budgets:

            for item in budgets:

                category = item["category"]
                budget = item["monthly_limit"]
                spent = item["spent"]
                remaining = item["remaining"]

                st.write(f"### {category}")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Budget",
                        f"₹{budget:,.2f}"
                    )

                with col2:
                    st.metric(
                        "Spent",
                        f"₹{spent:,.2f}"
                    )

                with col3:
                    st.metric(
                        "Remaining",
                        f"₹{remaining:,.2f}"
                    )

                # Budget progress
                if budget > 0:

                    progress = min(
                        max(spent / budget, 0),
                        1.0
                    )

                    st.progress(progress)

                    percentage = (
                        spent / budget
                    ) * 100

                    if percentage >= 100:
                        st.error(
                            f"⚠️ {category} budget exceeded "
                            f"({percentage:.1f}%)"
                        )

                    elif percentage >= 80:
                        st.warning(
                            f"⚠️ {category} budget is "
                            f"{percentage:.1f}% used"
                        )

                    else:
                        st.success(
                            f"✅ {percentage:.1f}% of "
                            f"{category} budget used"
                        )

        else:

            st.info("No budget data available.")

        st.divider()

        # ==================================================
        # SPENDING INTELLIGENCE
        # ==================================================

        st.header("🧠 Spending Intelligence")

        # --------------------------------------------------
        # TOP SPENDING CATEGORIES
        # --------------------------------------------------

        st.subheader("🔥 Top Spending Categories")

        if category_spending:

            category_cols = st.columns(
                min(len(category_spending), 4)
            )

            for index, item in enumerate(category_spending[:4]):

                with category_cols[index % len(category_cols)]:

                    st.metric(
                        item["category"],
                        f"₹{item['total']:,.2f}"
                    )

        else:

            st.info("No category spending data available.")

        # --------------------------------------------------
        # MONTHLY SPENDING TREND
        # --------------------------------------------------

        st.subheader("📈 Monthly Spending Trend")

        if monthly_spending:

            chart_data = {
                "Month": [],
                "Spending": []
            }

            for item in reversed(monthly_spending):

                chart_data["Month"].append(
                    f"{item['year']}-{item['month']:02d}"
                )

                chart_data["Spending"].append(
                    item["total"]
                )

            st.line_chart(
                chart_data,
                x="Month",
                y="Spending"
            )

        else:

            st.info("No monthly spending data available.")

        # --------------------------------------------------
        # TOP 5 EXPENSES
        # --------------------------------------------------

        st.subheader("💸 Top 5 Individual Expenses")

        if top_expenses:

            for index, expense in enumerate(top_expenses, start=1):

                merchant = expense["merchant_name"] or "Unknown"

                st.write(
                    f"**{index}. {merchant}** — "
                    f"₹{expense['amount']:,.2f} "
                    f"({expense['category']})"
                )

        else:

            st.info("No expense data available.")

        # --------------------------------------------------
        # OVER-BUDGET CATEGORIES
        # --------------------------------------------------

        st.subheader("⚠️ Categories Over Budget")

        if overspending:

            for item in overspending:

                st.error(
                    f"**{item['category']}**: "
                    f"Spent ₹{item['spent']:,.2f} "
                    f"vs Budget ₹{item['budget']:,.2f} "
                    f"→ Overspent by "
                    f"₹{item['overspent_by']:,.2f}"
                )

        else:

            st.success(
                "✅ No categories are currently over budget."
            )

    except Exception as e:

        st.error(
            f"{type(e).__name__}: {e}"
        )
        