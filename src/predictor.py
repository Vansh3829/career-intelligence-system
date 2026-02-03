# src/predictor.py

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class CareerPredictor:
    def __init__(self):
        self.model = joblib.load("model.pkl")
        self.tfidf = joblib.load("tfidf.pkl")
        self.edu_encoder = joblib.load("edu_encoder.pkl")
        self.scaler = joblib.load("scaler.pkl")

        self.jobs_df = self._load_jobs_data()

    # ---------------- SAFE CSV LOADER ----------------
    def _load_jobs_data(self):
        df = pd.read_csv(
            "data/raw/jobs.csv",
            encoding="utf-16",
            sep=None,
            engine="python",
            on_bad_lines="skip"
        )

        # Handle malformed CSV
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

    # ---------------- INPUT PROCESSING ----------------
    def preprocess_input(self, skills, experience, projects, ai_score, education):
        skills_vec = self.tfidf.transform([skills]).toarray()

        edu_encoded = (
            self.edu_encoder.transform([education])[0]
            if education in self.edu_encoder.classes_
            else 0
        )

        numeric = self.scaler.transform([[experience, projects, ai_score]])
        return np.hstack([skills_vec, numeric, [[edu_encoded]]])

    # ---------------- MARKET SALARY ----------------
    def market_salary_stats(self, role):
        role_df = self.jobs_df[
            self.jobs_df["Job"].str.contains(role, case=False, na=False)
        ].dropna(subset=["Mean_Salary"])

        if role_df.empty:
            return None

        return {
            "mean_salary": int(role_df["Mean_Salary"].mean())
        }

    # ---------------- COMPANY RECOMMENDATION ----------------
    def recommend_companies(self, skills, role, current_salary):
        role_jobs = self.jobs_df[
            self.jobs_df["Job"].str.contains(role, case=False, na=False)
        ].dropna(subset=["Skills", "Company", "Mean_Salary"])

        if role_jobs.empty:
            return []

        # 🔒 Only companies offering at least 10% hike
        role_jobs = role_jobs[
            role_jobs["Mean_Salary"] >= current_salary * 1.10
        ]

        if role_jobs.empty:
            return []

        # Skill similarity
        user_vec = self.tfidf.transform([skills])
        job_vecs = self.tfidf.transform(role_jobs["Skills"].astype(str))

        role_jobs["Skill_Match"] = cosine_similarity(
            user_vec, job_vecs
        )[0]

        # Salary normalization
        role_jobs["Salary_Score"] = (
            role_jobs["Mean_Salary"] / role_jobs["Mean_Salary"].max()
        )

        # Final score (salary prioritized)
        role_jobs["Final_Score"] = (
            0.6 * role_jobs["Salary_Score"]
            + 0.4 * role_jobs["Skill_Match"]
        )

        top = (
            role_jobs
            .sort_values("Final_Score", ascending=False)
            .head(10)
        )

        return top[["Company", "Mean_Salary", "Skill_Match"]].to_dict(
            orient="records"
        )

    # ---------------- MAIN PREDICTION ----------------
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
        X = self.preprocess_input(
            skills, experience, projects, ai_score, education
        )

        prob = self.model.predict_proba(X)[0][1]
        confidence = round(prob * 100, 2)

        hire_decision = "Hire" if prob >= 0.6 else "Reject"

        salary_stats = self.market_salary_stats(role)

        # ---------- ROLE SWITCH ----------
        if prob < 0.45:
            role_switch = True
            role_reason = (
                "Low hiring probability indicates limited growth in the current role"
            )
        else:
            role_switch = False
            role_reason = "Profile aligns well with the current role"

        # ---------- ABSOLUTE SALARY FLOOR ----------
        expected_min_salary = {
            0: 300000,
            1: 400000,
            2: 600000,
            3: 800000,
            4: 1000000
        }

        absolute_floor = expected_min_salary.get(experience, 600000)
        absolute_underpaid = current_salary < absolute_floor

        # ---------- RELATIVE MARKET CHECK ----------
        relative_underpaid = False
        if salary_stats:
            relative_underpaid = (
                current_salary < salary_stats["mean_salary"] * 0.85
            )

        # ---------- COMPANY SWITCH ----------
        if absolute_underpaid or relative_underpaid:
            company_switch = True
            company_reason = (
                "Your compensation is significantly below industry expectations "
                "for your experience and skill set"
            )
            recommended_companies = self.recommend_companies(
                skills, role, current_salary
            )

            if not recommended_companies:
                company_switch = False
                company_reason = (
                    "No companies currently offer a meaningful salary uplift"
                )
        else:
            company_switch = False
            company_reason = (
                "Your salary is competitive relative to market and experience"
            )
            recommended_companies = []

        # ---------- SALARY PREDICTION ----------
        hike = 0.35 if prob >= 0.75 else 0.20 if prob >= 0.6 else 0.10
        predicted_salary = int(current_salary * (1 + hike))

        return {
            "Hire Decision": hire_decision,
            "Confidence (%)": confidence,

            "Role Switch Recommended": role_switch,
            "Role Switch Reason": role_reason,

            "Company Switch Recommended": company_switch,
            "Company Switch Reason": company_reason,

            "Predicted Salary": predicted_salary,
            "Recommended Companies": recommended_companies
        }


# ---------------- TEST ----------------
if __name__ == "__main__":
    predictor = CareerPredictor()

    result = predictor.predict(
        skills="python angular ai ml",
        experience=2,
        projects=3,
        ai_score=75,
        education="Bachelor",
        current_salary=100000,
        role="Analyst"
    )

    for k, v in result.items():
        print(f"{k}: {v}")
