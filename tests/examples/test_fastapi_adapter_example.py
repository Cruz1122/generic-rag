import pytest

# Skip this entire module if fastapi or httpx is not installed
pytest.importorskip("fastapi")

from fastapi.testclient import TestClient
from examples.adapters.fastapi_adapter_example import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_answer_endpoint(client):
    payload = {"query": "Is the adapter online?", "top_k": 1}
    response = client.post("/answer", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "citations" in data
    assert "FastAPI Example" in data["answer"]
    assert len(data["citations"]) > 0
    assert data["citations"][0]["metadata"]["source"] == "api_docs"

def test_answer_validation(client):
    payload = {"query": "  "}
    response = client.post("/answer", json=payload)
    assert response.status_code == 400
    assert "Query cannot be empty" in response.json()["detail"]
