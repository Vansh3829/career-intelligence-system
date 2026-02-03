# src/feature_engineering.py

import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split


def load_resume_data(path="data/raw/resumes.csv"):
    """
    Load resumes dataset
    """
    df = pd.read_csv(path, encoding="utf-8", on_bad_lines="skip")
    return df


def preprocess_resumes(df):
    """
    Clean and preprocess resume data
    """

    # Drop rows with missing target
    df = df.dropna(subset=["Recruiter Decision"])

    # Fill missing values
    df["Skills"] = df["Skills"].fillna("")
    df["Certifications"] = df["Certifications"].fillna("None")
    df["Education"] = df["Education"].fillna("Unknown")

    # Convert numeric columns
    numeric_cols = [
        "Experience (Years)",
        "Projects Count",
        "AI Score (0-100)"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


def encode_features(df):
    """
    Encode text and categorical features
    """

    # ----- Encode Skills using TF-IDF -----
    tfidf = TfidfVectorizer(
        max_features=300,
        stop_words="english"
    )
    skill_features = tfidf.fit_transform(df["Skills"])

    # ----- Encode Education -----
    edu_encoder = LabelEncoder()
    df["Education_encoded"] = edu_encoder.fit_transform(df["Education"])

    # ----- Scale numeric features -----
    scaler = StandardScaler()
    numeric_features = scaler.fit_transform(
        df[["Experience (Years)", "Projects Count", "AI Score (0-100)"]]
    )

    return skill_features, numeric_features, df, tfidf, edu_encoder, scaler


def prepare_training_data():
    """
    Final ML-ready dataset
    """

    df = load_resume_data()
    df = preprocess_resumes(df)

    skill_features, numeric_features, df, tfidf, edu_encoder, scaler = encode_features(df)

    # Combine all features
    X = np.hstack([
        skill_features.toarray(),
        numeric_features,
        df[["Education_encoded"]].values
    ])

    # Target variable
    y = df["Recruiter Decision"].apply(
        lambda x: 1 if x.lower() == "hire" else 0
    )

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    return X_train, X_test, y_train, y_test, tfidf, edu_encoder, scaler


if __name__ == "__main__":
    X_train, X_test, y_train, y_test, _, _, _ = prepare_training_data()
    print("Feature Engineering Completed")
    print("Train shape:", X_train.shape)
    print("Test shape:", X_test.shape)
