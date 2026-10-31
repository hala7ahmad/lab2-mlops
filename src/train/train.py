from pathlib import Path

import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import f1_score, roc_auc_score


# Project paths
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "churn_v2.csv"
MODEL_PATH = ROOT / "model_retrained.joblib"


def main():
    # Load dataset
    df = pd.read_csv(DATA)

    # Select features and target
    numeric = ["tenure_months", "monthly_fee", "support_calls"]
    categorical = ["contract", "internet_service"]

    X = df[numeric + categorical]
    y = df["churn"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # Build model pipeline
    model = Pipeline([
        ("prep", ColumnTransformer([
            ("num", StandardScaler(), numeric),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ])),
        ("clf", LogisticRegression(max_iter=1000)),
    ])

    # Train model
    model.fit(X_train, y_train)

    # Evaluate model
    proba = model.predict_proba(X_test)[:, 1]

    print("F1:", round(f1_score(y_test, proba > 0.5), 3))
    print("AUC:", round(roc_auc_score(y_test, proba), 3))

    # Save trained model
    joblib.dump(model, MODEL_PATH)
    print(f"Saved {MODEL_PATH.name}")


if __name__ == "__main__":
    main()