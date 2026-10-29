from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_model_loads():
    from src.app.main import model
    assert model is not None


def test_invalid_input():
    response = client.post("/predict", json={
        "tenure_months": -5,
        "monthly_fees": 60.0,
        "contract": "month-to-month",
        "internet_service": "fiber",
        "support_calls": 0
    })
    assert response.status_code == 422
def test_zero_tenure():
    response = client.post("/predict", json={
        "tenure_months": 0,
        "monthly_fee": 60.0,
        "contract": "month-to-month",
        "internet_service": "fiber",
        "support_calls": 0
    })

    print(response.json())
    assert response.status_code == 200
    assert "churn_probability" in response.json()

def test_deterministic_prediction():
    data = {
        "tenure_months": 12,
        "monthly_fee": 60.0,
        "contract": "month-to-month",
        "internet_service": "fiber",
        "support_calls": 0
    }

    response1 = client.post("/predict", json=data)
    response2 = client.post("/predict", json=data)

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json() == response2.json()