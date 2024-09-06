import pytest
from fastapi.testclient import TestClient
from app.main import app 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, get_db
from app.cache import get_redis
from app.mocks import async_redis_mock  
from app.config import settings
# Configurações para o banco de dados em memória para testes
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name_test}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criação da aplicação FastAPI e cliente de teste
app.dependency_overrides[get_db] = lambda: TestingSessionLocal()
app.dependency_overrides[get_redis] = lambda: async_redis_mock

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # Criação das tabelas de banco de dados
    Base.metadata.create_all(bind=engine)
    # Iniciar uma nova transação
    connection = engine.connect()
    transaction = connection.begin()
    # Configurar o SessionLocal para usar a conexão de teste
    TestingSessionLocal.configure(bind=connection)
    yield
    # Reverter a transação e fechar a conexão
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(bind=engine)

def test_create_task():
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "title": "Test Task", "description": "Test Description", "completed": False}

def test_get_tasks(setup_db):
    # Cria uma nova tarefa
    client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    
    # Obtém a lista de tarefas
    response = client.get("/tasks/")
    
    # Verifica o status da resposta
    assert response.status_code == 200
    
    # Verifica o conteúdo da resposta
    tasks = response.json()
    
    # Verifica se a tarefa esperada está na lista
    task_found = any(task["title"] == "Test Task" and task["description"] == "Test Description" for task in tasks)
    assert task_found

def test_get_task_by_id():
    client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Task", "description": "Test Description", "completed": False}

def test_update_task():
    client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    response = client.put("/tasks/1", json={"title": "Updated Task", "description": "Updated Description"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Updated Task", "description": "Updated Description", "completed": False}

def test_create_task_invalid_data():
    response = client.post("/tasks/", json={"title": "", "description": "Test Description"})
    assert response.status_code == 422  # Unprocessable Entity

def test_update_task_invalid_data():
    client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    response = client.put("/tasks/1", json={"title": ""})
    assert response.status_code == 422  # Unprocessable Entity

def test_update_task_not_found():
    response = client.put("/tasks/999", json={"title": "Test Task", "description": "Test Description"})
    print(response)
    assert response.status_code == 404

def test_complete_task():
    client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    response = client.patch("/tasks/1")
    assert response.status_code == 200
    assert response.json()["completed"] is True

def test_delete_task():
    client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    response = client.delete("/tasks/1")
    assert response.status_code == 204
    response = client.get("/tasks/1")
    assert response.status_code == 404

def test_delete_task_not_found():
    response = client.delete("/tasks/999")
    assert response.status_code == 404

def test_get_tasks_cache():
    # Criação de novas tarefas
    client.post("/tasks/", json={"title": "Task 1", "description": "Test Cache 1"})
    client.post("/tasks/", json={"title": "Task 2", "description": "Test Cache 2"})
    
    # Recuperação da lista de tarefas
    response = client.get("/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    
    # Verificação do número de tarefas
    assert len(tasks) >= 2  # O número de tarefas deve ser pelo menos 2
