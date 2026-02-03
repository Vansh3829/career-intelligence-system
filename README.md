# 📈 Career Intelligence System (ML-Powered)

An Explainable Machine Learning system that analyzes a candidate’s profile and provides data-driven career insights, including:

-Hiring probability

-Role switch recommendation

-Company switch recommendation

-Salary growth prediction

Built using real datasets, ML models, and business logic, and deployed using Streamlit.

## Live Demo
https://career-intelligence-system.streamlit.app/

## Problem Statement

Many professionals struggle to answer questions like:

Should I switch my job or stay?

Am I underpaid for my experience?

Is my current role aligned with my skillset?

Most existing tools are rule-based or generic.

This project solves the problem using:

Machine Learning for hiring probability

Market salary analysis

Experience-based compensation benchmarks

Explainable decision logic

## System Architecture
User Input (Skills, Experience, Salary)
        ↓
Feature Engineering + Encoding
        ↓
ML Model (Hiring Probability)
        ↓
Business Logic Engine
        ↓
Career Recommendations + Salary Insight
        ↓
Streamlit UI

📊 Features
✅ ML-Driven Hiring Prediction

Predicts hiring probability using a trained ML classifier

Uses skills (TF-IDF), experience, projects, AI score, and education

🔁 Role Switch Recommendation

Based on hiring probability

Detects misalignment between profile and role

🏢 Company Switch Recommendation

## Uses:

Experience-based salary benchmarks

Market salary averages

Profile confidence

Avoids misleading recommendations

💰 Salary Growth Prediction

Predicts next salary growth (10–35%)

Depends on hiring probability

🔍 Explainable Output

Every decision comes with clear reasoning

No black-box outputs

## Datasets Used
Dataset	Purpose
Resume Dataset	Train hiring prediction model
Jobs Dataset	Market salary reference
Job Posts Dataset	Skill patterns
Company Dataset	Industry context

All datasets are stored locally under data/raw/

## Tech Stack
💻 Backend & ML

Python

Pandas, NumPy

Scikit-learn

TF-IDF Vectorizer

Logistic Regression / Classifier

Joblib (model persistence)

🎨 Frontend

Streamlit

Matplotlib (minimal usage)

🛠 Tools

Git & GitHub

Streamlit Cloud (deployment)

## Project Structure
career-intelligence-system/
│
├── app.py                    # Streamlit UI
├── requirements.txt
├── README.md
│
├── data/
│   └── raw/
│       ├── resumes.csv
│       ├── jobs.csv
│       ├── job_post.csv
│       └── companies.csv
│
├── src/
│   ├── predictor.py          # Core ML + decision logic
│   ├── train_model.py        # Model training
│   ├── feature_engineering.py
│   ├── resume_parser.py
│   └── skill_mapper.py
│
├── model.pkl
├── tfidf.pkl
├── scaler.pkl
└── edu_encoder.pkl

⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/<your-username>/career-intelligence-system.git
cd career-intelligence-system

2️⃣ Create Virtual Environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Application
streamlit run app.py
