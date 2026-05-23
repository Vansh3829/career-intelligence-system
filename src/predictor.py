import joblib
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class CareerPredictor:
    def __init__(self):
        # ---------------- Load trained artifacts ----------------
        self.model = joblib.load("model.pkl")
        self.tfidf = joblib.load("tfidf.pkl")
        self.edu_encoder = joblib.load("edu_encoder.pkl")
        self.scaler = joblib.load("scaler.pkl")
        
        # FIXED: Core CSV reference loaded FIRST before calculations fire
        self.jobs_df = self._load_jobs_data()

    # ---------------- DYNAMIC COSINE SIMILARITY ENGINE ----------------
    def calculate_skill_alignment(self, user_role, user_skills):
        if self.jobs_df.empty:
            return 1.0  # Fallback if reference dataset is physically missing
            
        # Extract target records matching the designating input role
        role_matches = self.jobs_df[self.jobs_df["Job"].str.contains(user_role, case=False, na=False)]
        
        if role_matches.empty:
            return 1.0  # Safe boundary fallback for unique custom job titles
            
        # Aggregate all matching baseline skills from the dataset row entries
        market_skills_pool = " ".join(role_matches["Skills"].fillna("").astype(str))
        
        # FIXED: Reshaping text transformations into explicit 2D Scikit matrices
        user_vector = self.tfidf.transform([user_skills])
        market_vector = self.tfidf.transform([market_skills_pool])
        
        similarity_score = cosine_similarity(user_vector, market_vector)
        return float(similarity_score[0][0])

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
            
        if df.shape[1] == 1:
            df = df.iloc[:, 0].str.split(",", expand=True)
            df.columns = [
                "ID", "Job", "Jobs_Group", "Profile", "Remote", "Company", "Location", 
                "City", "State", "Salary", "Frequency_Salary", "Low_Salary", 
                "High_Salary", "Mean_Salary", "Skills"
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

    # ---------------- MARKET SALARY REF ----------------
    def market_salary_mean(self, role):
        if self.jobs_df.empty:
            return None
        role_df = self.jobs_df[
            self.jobs_df["Job"].str.contains(role, case=False, na=False)
        ].dropna(subset=["Mean_Salary"])
        if role_df.empty:
            return None
        return int(role_df["Mean_Salary"].mean())

    # ---------------- EXPERIENTIAL COMPENSATION REFERENCE ----------------
    def expected_salary_by_experience(self, exp):
        if exp <= 1:
            return 350000
        elif exp <= 3:
            return 700000
        elif exp <= 5:
            return 1200000
        elif exp <= 8:
            return 2000000
        else:
            return 3000000 

    # ---------------- MAIN PREDICTION EXECUTION PIPELINE ----------------
    def predict(
        self, skills, experience, projects, ai_score, education, current_salary, role
    ):
        # Machine learning inference metrics tracking
        X = self.preprocess_input(skills, experience, projects, ai_score, education)
        prob = self.model.predict_proba(X)[0][1]
        confidence = round(prob * 100, 2)
        hire_decision = "Hire" if prob >= 0.6 else "Reject"

        # Calculate mathematical similarity map score directly against jobs database baseline
        alignment_score = self.calculate_skill_alignment(role, skills)

        # Dynamic, non-hardcoded threshold analysis checks
        if alignment_score < 0.15:
            role_switch = True
            role_reason = (
                f"Your entered skills show a very low market alignment score ({round(alignment_score * 100, 1)}%) "
                f"with typical industry expectations for a '{role}' position. A domain transition is recommended."
            )
        elif prob < 0.45:
            role_switch = True
            role_reason = "Hiring probability for the current profile designation track is low, indicating a misalignment."
        else:
            role_switch = False
            role_reason = f"Your skills show a stable alignment match ({round(alignment_score * 100, 1)}%) with industry role expectations."

        # ---------------- COMPANY SWITCH LOGIC ----------------
        expected_salary = self.expected_salary_by_experience(experience)
        absolute_underpaid = current_salary < expected_salary * 0.7
        market_mean = self.market_salary_mean(role)
        relative_underpaid = (
            market_mean is not None and current_salary < market_mean * 0.75
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

        return {
            "Hire Decision": hire_decision,
            "Confidence (%)": confidence,
            "Role Switch Recommended": role_switch,
            "Role Switch Reason": role_reason,
            "Company Switch Recommended": company_switch,
            "Company Switch Reason": company_reason,
            "Predicted Salary": predicted_salary
        }

# ---------------- LOCAL RUN CONTROLS ----------------
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
