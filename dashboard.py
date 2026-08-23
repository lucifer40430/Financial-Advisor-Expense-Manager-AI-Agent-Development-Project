import streamlit as st

from backend.database.financial_analysis import (
    get_financial_summary
)


def show_dashboard(user_id):

    st.header("📊 Financial Dashboard")

    try:
        summary = get_financial_summary(user_id)

        total_spending = summary["total_spending"]
        categories = summary["category_spending"]
        budgets = summary["budget_analysis"]

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

    except Exception as e:

        st.error(
            f"{type(e).__name__}: {e}"
        )