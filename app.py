# app.py

import streamlit as st
from src.predictor import CareerPredictor

# -----------------------------
# App Config
# -----------------------------
st.set_page_config(
    page_title="Career Intelligence System",
    page_icon="📈",
    layout="centered"
)

st.title("📈 Career Intelligence System")
st.caption("Explainable ML-powered career & salary insights")

# -----------------------------
# Load Predictor
# -----------------------------
@st.cache_resource
def load_predictor():
    return CareerPredictor()

predictor = load_predictor()

# -----------------------------
# User Inputs
# -----------------------------
st.header("👤 Candidate Details")

skills = st.text_area(
    "Skills",
    placeholder="python, sql, machine learning, data analysis"
)

experience = st.number_input("Experience (Years)", 0, 40, 2)
projects = st.number_input("Projects", 0, 50, 3)
ai_score = st.slider("AI Score", 0, 100, 75)
education = st.selectbox(
    "Education",
    ["Bachelor", "Master", "PhD", "Diploma", "Other"]
)
role = st.text_input("Current Role", "Data Analyst")
current_salary = st.number_input(
    "Current Salary (₹)",
    min_value=100000,
    step=50000,
    value=600000
)

# -----------------------------
# Prediction
# -----------------------------
st.markdown("---")

if st.button("🔮 Analyze Career"):
    if not skills.strip():
        st.error("Please enter your skills.")
    else:
        result = predictor.predict(
            skills,
            experience,
            projects,
            ai_score,
            education,
            current_salary,
            role
        )

        st.success("Analysis Completed")

        # -----------------------------
        # Summary Metrics
        # -----------------------------
        st.subheader("📊 Decision Summary")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Hire Decision", result["Hire Decision"])
            st.metric("Confidence", f"{result['Confidence (%)']}%")

        with col2:
            st.metric(
                "Role Switch",
                "Yes" if result["Role Switch Recommended"] else "No"
            )
            st.metric(
                "Company Switch",
                "Yes" if result["Company Switch Recommended"] else "No"
            )

        # -----------------------------
        # Explanation
        # -----------------------------
        st.subheader("💡 Explanation")

        st.markdown("### 🔁 Role Switch Analysis")
        st.info(result["Role Switch Reason"])

        st.markdown("### 🏢 Company Switch Analysis")
        st.info(result["Company Switch Reason"])

        # -----------------------------
        # Salary Insight
        # -----------------------------
        st.subheader("💰 Salary Insight")
        st.metric(
            "Predicted Salary (Next Growth)",
            f"₹{result['Predicted Salary']:,}"
        )

        

        # -----------------------------
        # Company Recommendations
        # -----------------------------
        

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Built with ❤️ using Explainable Machine Learning")
