import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, get_db
from app.config import settings

# Cria uma conexão temporária com o banco de dados SQLite para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria a base de dados de teste
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_task(setup_database):
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] == False
    
def test_create_task_missing_title(setup_database):
    response = client.post("/tasks/", json={"description": "Test Description"})
    assert response.status_code == 422
    assert "title" in response.json()["detail"][0]["loc"]

def test_create_task_missing_description(setup_database):
    response = client.post("/tasks/", json={"title": "Test Task"})
    assert response.status_code == 422
    assert "description" in response.json()["detail"][0]["loc"]

def test_get_tasks(setup_database):
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_task_by_id(setup_database):
    # Primeiro, crie uma tarefa para poder testá-la
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    task_id = response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test Task"
    
def test_get_task_fields(setup_database):
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    task_id = response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    data = response.json()
    assert "completed" in data
    assert "extra_field" not in data  # Supondo que "extra_field" não deve existir

def test_update_task(client: TestClient, setup_database: None):
    # Cria uma nova tarefa
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    task_id = response.json()["id"]
    
    # Atualiza a tarefa sem o campo 'completed'
    response = client.put(f"/tasks/{task_id}", json={"title": "Updated Task", "description": "Updated Description"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated Description"
    assert "completed" in data  # Verifica que o campo 'completed' está presente
    assert data["completed"] is False  # Supondo que o campo 'completed' deve ser False após atualização PUT

def test_update_task_invalid_data(setup_database):
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    task_id = response.json()["id"]
    
    response = client.put(f"/tasks/{task_id}", json={"title": ""})  # título vazio
    assert response.status_code == 422
    
def test_update_nonexistent_task(setup_database):
    response = client.put("/tasks/999999", json={"title": "Updated Task", "description": "Updated Description"})
    assert response.status_code == 404

def test_complete_task(setup_database):
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    task_id = response.json()["id"]

    response = client.patch(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] == True

def test_delete_task(setup_database):
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    task_id = response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404

def test_delete_nonexistent_task(setup_database):
    response = client.delete("/tasks/999999")
    assert response.status_code == 404
