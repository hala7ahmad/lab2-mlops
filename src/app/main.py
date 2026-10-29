"""Lab 1 FastAPI skeleton: serves the model you saved from the notebook.

Run it by hand (this is Round 1 of the race):
    uvicorn app.main:app --port 8000
Then send predictions with curl (see sample_request.json).
"""
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

MODEL_PATH = "model.joblib"   # where the notebook saves the model (yes, hard-coded on purpose)
FEATURES = ["tenure_months", "monthly_fee", "contract", "internet_service", "support_calls"]
class CustomerInput(BaseModel):
    tenure_months: int = Field(ge=0)
    monthly_fee: float = Field(ge=0)
    contract: str
    internet_service: str
    support_calls: int = Field(ge=0)
app = FastAPI(title="AI381 Lab 1 churn API")
model = joblib.load(MODEL_PATH)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(customer: CustomerInput):
    X = pd.DataFrame([customer.model_dump()])[FEATURES]
    p = float(model.predict_proba(X)[0, 1])
    return {"churn_probability": round(p, 3)}
