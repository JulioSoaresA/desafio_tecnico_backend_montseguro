# Desafio Técnico Backend
Repositório relacionado ao Desafio Técnico Backend do Montseguro Corretora

# pythonToDoList

## Desenvolvimento de um Microserviço de To-Do List

- **Desafio Técnico**: Desenvolvimento de um Microserviço de To-Do List
- **Empresa**: Montseguro
- **Vaga**: Desenvolvedor Back End Python Pleno
- **Nome**: Júlio César Almeida Soares

---

## Descrição

Este repositório contém o código relacionado ao Desafio Técnico Backend para a Montseguro Corretora, com o objetivo de desenvolver um microserviço para gerenciamento de tarefas (To-Do List).

---

## Linguagens e Tecnologias Utilizadas

- **Python**
- **Banco de Dados**: SQLite (para desenvolvimento) e PostgreSQL (produção)
- **IDE**: VSCode
- **Bibliotecas Python**: FastAPI, Uvicorn, SQLAlchemy
- **Docker**: Para facilitar a implantação e execução do ambiente

---

## Instruções para Rodar o Projeto

### Guia de Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/JulioSoaresA/desafio_tecnico_backend_montseguro.git
2. Acesse o diretório do projeto:
   ```bash
   cd todo_list

### Instalação de Ambiente Virtual
  1. Baixe este repositório e entre no diretório do projeto.
  2. Crie um ambiente virtual utilizando o VirtualEnv:
     ```bash
     python -m venv venv
  3. Ativando o ambiente virtual:
     - No Linux:
       ```bash
       source venv/bin/activate

      - No Windows:
        ```bash
        .\venv\Scripts\activate.ps1
  4. Instale as dependências:
     ```bash
     pip install -r requirements.txt
     ```

  ### Instruções para Rodar o Projeto Localmente
  Para rodar o projeto com o Uvicorn localmente, utilize o seguinte comando:
  ```bash
    uvicorn app:app --reload
  ```
  Isso iniciará o servidor e você poderá acessar a documentação interativa da API via http://127.0.0.1:8000/docs.

  ---

  ### Instruções para Rodar o Projeto com Docker
  Se preferir rodar o projeto usando Docker, basta executar:
  ```bash
  docker-compose up --build
  ```
  Isso irá construir e iniciar o container, incluindo o banco de dados e o servidor FastAPI.

  ---

## Estrutura do projeto
```bash
├── app
│   ├── cache.py
│   ├── config.py
│   ├── db.py
│   ├── __init__.py
│   ├── main.py
│   ├── mocks.py
│   ├── models.py
│   ├── routers
│   │   └── task.py
│   └── schemas.py
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
├── test.db
└── tests
    ├── conftest.py
    ├── __init__.py
    └── test_task.py
```

---

## Endpoints da API
Abaixo estão os principais endpoints da API To-Do List:

### Tarefas:
- ```GET /tasks/``` - Listar todas as tarefas
- ```POST /tasks/``` - Criar uma nova tarefa
- ```PUT /tasks/{task_id}``` - Atualizar uma tarefa existente
- ```PATCH /tasks/{task_id}```- Marcar tarefa como concluída
- ```GET /tasks/{task_id}``` - Buscar uma tarefa por ID
- ```DELETE /tasks/{task_id}``` - Excluir uma tarefa

### Exemplo de Requisição para Criar uma Tarefa
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/tasks/' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Nova Tarefa",
    "description": "Descrição da tarefa",
    "completed": false
  }'
```

---

## Observações
Este projeto foi desenvolvido como parte de um desafio técnico, com foco em:
  - Práticas de desenvolvimento de Microserviços
  - Uso de FastAPI para criação de APIs
  - Implementação de operações CRUD (Create, Read, Update, Delete)
