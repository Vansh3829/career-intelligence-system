# src/predictor.py

import joblib
import numpy as np
import pandas as pd


class CareerPredictor:
    def __init__(self):
        # Load trained artifacts
        self.model = joblib.load("model.pkl")
        self.tfidf = joblib.load("tfidf.pkl")
        self.edu_encoder = joblib.load("edu_encoder.pkl")
        self.scaler = joblib.load("scaler.pkl")

        # Load jobs dataset (used ONLY for market salary reference)
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

    # ---------------- MARKET SALARY (OPTIONAL REFERENCE) ----------------
    def market_salary_mean(self, role):
        if self.jobs_df.empty:
            return None

        role_df = self.jobs_df[
            self.jobs_df["Job"].str.contains(role, case=False, na=False)
        ].dropna(subset=["Mean_Salary"])

        if role_df.empty:
            return None

        return int(role_df["Mean_Salary"].mean())

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
        # Model inference
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
                "Hiring probability is low for the current role, suggesting "
                "limited alignment or growth potential."
            )
        else:
            role_switch = False
            role_reason = (
                "Your skill set and experience align well with the current role."
            )

        # ---------------- COMPANY SWITCH LOGIC (FIXED & CLEAN) ----------------

        # Experience-based minimum salary benchmark (India – conservative)
        experience_salary_floor = {
            0: 250000,
            1: 350000,
            2: 500000,
            3: 700000,
            4: 900000,
            5: 1100000
        }

        expected_salary = experience_salary_floor.get(
            experience, 700000
        )

        # Absolute underpayment check (MOST IMPORTANT)
        absolute_underpaid = current_salary < expected_salary * 0.8

        # Relative market check (secondary)
        market_mean = self.market_salary_mean(role)
        relative_underpaid = (
            market_mean is not None
            and current_salary < market_mean * 0.85
        )

        high_confidence = prob >= 0.65

        if high_confidence and (absolute_underpaid or relative_underpaid):
            company_switch = True
            company_reason = (
                f"Your current salary (₹{current_salary:,}) is significantly below "
                f"expected compensation for {experience} years of experience "
                f"(₹{expected_salary:,}+). With a strong profile, switching "
                f"companies is recommended."
            )
        else:
            company_switch = False
            company_reason = (
                "Your compensation is reasonably aligned with experience-based "
                "expectations, so a company switch is not strongly recommended."
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
        experience=4,
        projects=3,
        ai_score=71,
        education="Bachelor",
        current_salary=250000,
        role="Software Developer"
    )

    for k, v in result.items():
        print(f"{k}: {v}")
