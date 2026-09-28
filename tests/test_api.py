from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Aegis is running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "aegis-api"


def test_total_revenue_endpoint():
    response = client.get(
        "/api/v1/data/revenue"
    )

    assert response.status_code == 200
    assert response.json()["total_revenue"] == 109000.0


def test_monthly_revenue_endpoint():
    response = client.get(
        "/api/v1/data/monthly-revenue"
    )

    assert response.status_code == 200

    data = response.json()

    monthly_revenue = data["monthly_revenue"]

    assert len(monthly_revenue) == 2
    assert monthly_revenue[0]["revenue"] == 105000
    assert monthly_revenue[1]["revenue"] == 4000