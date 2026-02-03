# src/predictor.py

import joblib
import numpy as np
import pandas as pd


class CareerPredictor:
    def __init__(self):
        # ---------------- Load trained artifacts ----------------
        self.model = joblib.load("model.pkl")
        self.tfidf = joblib.load("tfidf.pkl")
        self.edu_encoder = joblib.load("edu_encoder.pkl")
        self.scaler = joblib.load("scaler.pkl")

        # Jobs dataset is used ONLY for market salary reference
        self.jobs_df = self._load_jobs_data()

    # ---------------- SAFE CSV LOADER ----------------
    def _load_jobs_data(self):
        try:
            df = pd.read_csv(
                "data/raw/jobs.csv",
                encoding="utf-16",
                sep=None,
                engine="python",
                on_bad_lines="skip"
            )
        except Exception:
            return pd.DataFrame()

        # Handle badly formatted single-column CSV
        if df.shape[1] == 1:
            df = df.iloc[:, 0].str.split(",", expand=True)
            df.columns = [
                "ID", "Job", "Jobs_Group", "Profile", "Remote",
                "Company", "Location", "City", "State",
                "Salary", "Frequency_Salary",
                "Low_Salary", "High_Salary", "Mean_Salary",
                "Skills"
            ]

        df.columns = df.columns.str.strip()

        for col in ["Low_Salary", "High_Salary", "Mean_Salary"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        return df

    # ---------------- INPUT PREPROCESSING ----------------
    def preprocess_input(self, skills, experience, projects, ai_score, education):
        skills_vec = self.tfidf.transform([skills]).toarray()

        edu_encoded = (
            self.edu_encoder.transform([education])[0]
            if education in self.edu_encoder.classes_
            else 0
        )

        numeric = self.scaler.transform([[experience, projects, ai_score]])

        return np.hstack([skills_vec, numeric, [[edu_encoded]]])

    # ---------------- MARKET SALARY (OPTIONAL) ----------------
    def market_salary_mean(self, role):
        if self.jobs_df.empty:
            return None

        role_df = self.jobs_df[
            self.jobs_df["Job"].str.contains(role, case=False, na=False)
        ].dropna(subset=["Mean_Salary"])

        if role_df.empty:
            return None

        return int(role_df["Mean_Salary"].mean())

    # ---------------- EXPERIENCE → SALARY BENCHMARK ----------------
    def expected_salary_by_experience(self, exp):
        """
        Conservative Indian market baseline (LPA converted to INR)
        """
        if exp <= 1:
            return 350000
        elif exp <= 3:
            return 700000
        elif exp <= 5:
            return 1200000
        elif exp <= 8:
            return 2000000
        else:
            return 3000000  # 9+ years

    # ---------------- MAIN PREDICTION LOGIC ----------------
    def predict(
        self,
        skills,
        experience,
        projects,
        ai_score,
        education,
        current_salary,
        role
    ):
        # --------- ML inference ---------
        X = self.preprocess_input(
            skills, experience, projects, ai_score, education
        )

        prob = self.model.predict_proba(X)[0][1]
        confidence = round(prob * 100, 2)

        hire_decision = "Hire" if prob >= 0.6 else "Reject"

        # ---------------- ROLE SWITCH LOGIC ----------------
        if prob < 0.45:
            role_switch = True
            role_reason = (
                "Hiring probability for the current role is low, indicating limited "
                "alignment or future growth potential."
            )
        else:
            role_switch = False
            role_reason = (
                "Your skills and experience align well with the current role."
            )

        # ---------------- COMPANY SWITCH LOGIC ----------------
        expected_salary = self.expected_salary_by_experience(experience)

        absolute_underpaid = current_salary < expected_salary * 0.7

        market_mean = self.market_salary_mean(role)
        relative_underpaid = (
            market_mean is not None
            and current_salary < market_mean * 0.75
        )

        high_confidence = prob >= 0.65

        if high_confidence and absolute_underpaid:
            company_switch = True
            company_reason = (
                f"With {experience} years of experience, expected compensation is "
                f"₹{expected_salary:,}+ but your current salary is ₹{current_salary:,}. "
                "This indicates severe underpayment. A company switch is strongly recommended."
            )
        elif high_confidence and relative_underpaid:
            company_switch = True
            company_reason = (
                "Your salary is significantly below the current market average for this role. "
                "With a strong profile, switching companies can unlock better compensation."
            )
        else:
            company_switch = False
            company_reason = (
                "Your compensation is reasonably aligned with experience-based and market "
                "benchmarks. A company switch is optional rather than necessary."
            )

        # ---------------- SALARY GROWTH PREDICTION ----------------
        if prob >= 0.75:
            hike = 0.35
        elif prob >= 0.6:
            hike = 0.20
        else:
            hike = 0.10

        predicted_salary = int(current_salary * (1 + hike))

        # ---------------- FINAL OUTPUT ----------------
        return {
            "Hire Decision": hire_decision,
            "Confidence (%)": confidence,

            "Role Switch Recommended": role_switch,
            "Role Switch Reason": role_reason,

            "Company Switch Recommended": company_switch,
            "Company Switch Reason": company_reason,

            "Predicted Salary": predicted_salary
        }


# ---------------- LOCAL TEST ----------------
if __name__ == "__main__":
    predictor = CareerPredictor()

    result = predictor.predict(
        skills="javascript react node mongodb",
        experience=10,
        projects=10,
        ai_score=75,
        education="Bachelor",
        current_salary=350000,
        role="SDE"
    )

    for k, v in result.items():
        print(f"{k}: {v}")
