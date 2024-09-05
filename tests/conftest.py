import pytest
from fastapi.testclient import TestClient
from app.main import app  # Certifique-se de que o caminho está correto

@pytest.fixture(scope="module")
def client():
    return TestClient(app)
