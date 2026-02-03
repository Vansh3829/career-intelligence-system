# src/train_model.py

import joblib
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from feature_engineering import prepare_training_data


def train_models():
    """
    Train ML models and select the best one
    """

    # Load prepared data
    X_train, X_test, y_train, y_test, tfidf, edu_encoder, scaler = prepare_training_data()

    # ---------------------------
    # Model 1: Logistic Regression
    # ---------------------------
    lr = LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    )
    lr.fit(X_train, y_train)

    lr_preds = lr.predict(X_test)
    lr_acc = accuracy_score(y_test, lr_preds)

    print("\nLogistic Regression Accuracy:", lr_acc)
    print(classification_report(y_test, lr_preds))

    # ---------------------------
    # Model 2: Random Forest
    # ---------------------------
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        class_weight="balanced"
    )
    rf.fit(X_train, y_train)

    rf_preds = rf.predict(X_test)
    rf_acc = accuracy_score(y_test, rf_preds)

    print("\nRandom Forest Accuracy:", rf_acc)
    print(classification_report(yy_test := y_test, rf_preds))

    # ---------------------------
    # Select Best Model
    # ---------------------------
    if rf_acc >= lr_acc:
        best_model = rf
        best_model_name = "RandomForest"
        best_acc = rf_acc
    else:
        best_model = lr
        best_model_name = "LogisticRegression"
        best_acc = lr_acc

    print(f"\nBest Model Selected: {best_model_name} (Accuracy: {best_acc})")

    # ---------------------------
    # Save model & preprocessors
    # ---------------------------
    joblib.dump(best_model, "model.pkl")
    joblib.dump(tfidf, "tfidf.pkl")
    joblib.dump(edu_encoder, "edu_encoder.pkl")
    joblib.dump(scaler, "scaler.pkl")

    print("\nModel and preprocessors saved successfully!")


if __name__ == "__main__":
    train_models()
