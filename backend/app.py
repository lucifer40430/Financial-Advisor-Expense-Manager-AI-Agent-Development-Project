import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Make backend package available
sys.path.insert(0, str(PROJECT_ROOT))


import streamlit as st
from backend.database.financial_profile import save_profile, get_profile
from backend.ocr.vision_ocr import vision_transcribe
from backend.expense.expense_parser import parse_expense
from backend.database.expense_db import save_expense
from backend.ai.financial_advisor import get_financial_advice
from backend.dashboard import show_dashboard

st.set_page_config(
    page_title="FinSight AI",
    page_icon="💰",
    layout="wide"
)

st.title("💰 FinSight AI")
st.subheader("AI Financial Advisor")

USER_ID = 1
# ============================================================
# FINANCIAL PROFILE
# ============================================================

st.header("👤 Financial Profile")

existing_profile = get_profile(USER_ID)

with st.form("financial_profile_form"):

    monthly_income = st.number_input(
        "Monthly Income (₹)",
        min_value=0.0,
        value=float(existing_profile["monthly_income"]) if existing_profile else 0.0,
        step=1000.0
    )

    current_savings = st.number_input(
        "Current Savings (₹)",
        min_value=0.0,
        value=float(existing_profile["current_savings"]) if existing_profile else 0.0,
        step=1000.0
    )

    fixed_monthly_expenses = st.number_input(
        "Fixed Monthly Expenses (₹)",
        min_value=0.0,
        value=float(existing_profile["fixed_monthly_expenses"]) if existing_profile else 0.0,
        step=1000.0
    )

    monthly_debt_payment = st.number_input(
        "Monthly EMI / Debt Payment (₹)",
        min_value=0.0,
        value=float(existing_profile["monthly_debt_payment"]) if existing_profile else 0.0,
        step=500.0
    )

    financial_goal = st.text_input(
        "Financial Goal",
        value=existing_profile["financial_goal"] if existing_profile else "",
        placeholder="e.g. Buy a bike"
    )

    goal_amount = st.number_input(
        "Goal Amount (₹)",
        min_value=0.0,
        value=float(existing_profile["goal_amount"]) if existing_profile else 0.0,
        step=1000.0
    )

    goal_deadline = st.date_input(
        "Goal Deadline",
        value=existing_profile["goal_deadline"] if existing_profile else None
    )

    risk_preference = st.selectbox(
        "Risk Preference",
        ["Conservative", "Moderate", "Aggressive"],
        index=(
            ["Conservative", "Moderate", "Aggressive"].index(
                existing_profile["risk_preference"]
            )
            if existing_profile
            and existing_profile["risk_preference"] in
            ["Conservative", "Moderate", "Aggressive"]
            else 1
        )
    )

    save_button = st.form_submit_button("💾 Save Profile")

    if save_button:

        try:

            save_profile(
                user_id=USER_ID,
                monthly_income=monthly_income,
                current_savings=current_savings,
                fixed_monthly_expenses=fixed_monthly_expenses,
                monthly_debt_payment=monthly_debt_payment,
                financial_goal=financial_goal,
                goal_amount=goal_amount,
                goal_deadline=goal_deadline,
                risk_preference=risk_preference
            )

            st.success("✅ Financial profile saved successfully!")

        except Exception as e:

            st.error(
                f"{type(e).__name__}: {e}"
            )

# ============================================================
# EXPENSE UPLOAD
# ============================================================

st.header("📤 Add Expense")

uploaded_file = st.file_uploader(
    "Upload payment screenshot",
    type=["png", "jpg", "jpeg", "webp"]
)


if uploaded_file:

    st.image(
        uploaded_file,
        caption="Payment Screenshot",
        width=400
    )


    if st.button("Process Expense"):

        try:

            # ------------------------------------------------
            # Save temporary image
            # ------------------------------------------------

            temp_path = "payment_temp.png"

            with open(temp_path, "wb") as file:
                file.write(uploaded_file.getbuffer())


            # ------------------------------------------------
            # OCR
            # ------------------------------------------------

            with st.spinner("Reading payment screenshot..."):

                ocr_text = vision_transcribe(
                    __import__("pathlib").Path(temp_path)
                )


            st.subheader("🔍 OCR Result")

            st.text_area(
                "Extracted Text",
                ocr_text,
                height=200
            )


            # ------------------------------------------------
            # Parse expense
            # ------------------------------------------------

            with st.spinner(
                "Extracting expense information..."
            ):

                expense = parse_expense(
                    ocr_text
                )


            st.subheader("💳 Expense Details")

            st.json(expense)


            # ------------------------------------------------
            # Save MySQL
            # ------------------------------------------------

            with st.spinner(
                "Saving expense..."
            ):

                expense_id = save_expense(
                    expense=expense,
                    user_id=USER_ID,
                    image_path=temp_path
                )


            st.success(
                f"✅ Expense saved successfully! "
                f"ID: {expense_id}"
            )


        except Exception as e:

            st.error(
                f"{type(e).__name__}: {e}"
            )
st.divider()

show_dashboard(USER_ID)            
        # ============================================================
# AI FINANCIAL ADVISOR
# ============================================================

st.divider()

st.header("🤖 Ask FinSight AI")

question = st.text_input(
    "Ask your financial question",
    placeholder="e.g. Am I spending too much on food?"
)

if st.button("Ask FinSight AI"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        try:

            with st.spinner("FinSight AI is thinking..."):

                answer = get_financial_advice(
                    user_id=USER_ID,
                    question=question
                )

            st.subheader("💡 FinSight AI")
            st.write(answer)

        except Exception as e:

            st.error(
                f"{type(e).__name__}: {e}"
            )    
