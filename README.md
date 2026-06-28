# 📈 Career Intelligence System (ML-Powered)

An enterprise-grade, explainable machine learning platform that analyzes candidate profiles to deliver data-driven career diagnostics, talent alignment metrics, and compensation forecasting benchmarks.

**Live System Link:** https://career-intelligence-system.streamlit.app/

---

##  System Architecture Overview

The platform uses a decoupled client-server emulation architecture built purely inside Python:

```text
User Input Hub (Designation, Skills, Experience)
      ↓
Feature Engineering Pipeline (Data Cleaning & Encoding)
      ↓
Vector Mapping Engine [TfidfVectorizer & Scaler Transformation]
      ↓
      ├─► ML Inference Core (Hiring Probability / Logistic Regression)
      
            ↓
Data-Driven Decision Engine
      ↓
UI Display Grid (Streamlit +  Plotly Charts)
```

---

##  Key Technical Features

### 1. Skill Alignment Matrix
Replaced rigid keyword rules with an advanced semantic parsing engine. The system performs **Cosine Similarity** computations, comparing user-entered skills directly against industry baseline benchmarks extracted from a localized market dataset (`jobs.csv`). It flags path mismatches mathematically if text similarity drops below a specific threshold.

### 2. High-Fidelity Decision Summaries
Generates binary classifier decisions ("Hire" vs. "Reject") using trained logistic regression probability parameters, accompanied by explicit confidence scores.

### 3. Predictive Compensation Anchoring
Calculates compensation ceiling projections by tracking local market averages and experience-based baselines, rendering insights onto high-contrast interactive Plotly data visualizations.

### 4. Explainable Career Path Mapping
Cross-references profiles to dynamically recommend strategic role adaptations and organizational adjustments with clear, plain-language reasoning.

---

## Tech Stack & Dependencies

* **Frontend Engine:** Streamlit Core (Enhanced with custom glassmorphic HTML/CSS canvas injection layers)
* **Visual Graphics Matrix:** Plotly Express & Graph Objects 
* **Machine Learning Pipeline:** Scikit-Learn (TfidfVectorizer, StandardScaler, LabelEncoder)
* **Model Serialization:** Joblib
* **Data Processing Layer:** Pandas, NumPy

---

##  Project Structure

```text
career-intelligence-system/
│
├── app.py                      # Premium UI Grid Configuration
├── requirements.txt            # System Dependency Tracking manifest
├── README.md                   # System Documentation Hub
│
├── data/raw/
│   ├── resumes.csv             # Classifier Training Pool Baseline
│   ├── jobs.csv                # Market Reference Salary & Skill Database
│   ├── job_post.csv            # Industry Skill Pattern Trackers
│   └── companies.csv           # Corporate Sector Demographics
│
├── src/
│   ├── predictor.py            # Cosine Similarity Engine & ML Predictor Core
│   ├── train_model.py          # Serialized Pipeline Model Generator
│   └── feature_engineering.py  # Matrix Preprocessing Script Layers
│
├── model.pkl                   # Trained Binary Classifier Model
├── tfidf.pkl                   # Serialized Text Vectorizer Model
├── scaler.pkl                  # Serialized Numerical Scaling Configuration
└── edu_encoder.pkl             # Serialized Categorical Categorization Matrix
```

---

##  Installation & Local Setup

### 1. Clone the Workspace Repository
```bash
git clone https://github.com
cd career-intelligence-system
```

### 2. Initialize and Activate Your Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # macOS / Linux
# venv\Scripts\activate  # Windows Alternative Prompt
```

### 3. Install Operational Package Layers
```bash
pip install -r requirements.txt
```

### 4. Boot up the Ecosystem Server
```bash
streamlit run app.py
```

---


