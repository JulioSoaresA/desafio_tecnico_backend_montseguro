# Desafio Técnico Backend
Repositório relacionado ao Desafio Técnico Backend do Montseguro Corretora

# pythonToDoList
## Desenvolvimento de um Microserviço de To-Do List
- Desafio Técnico: Desenvolvimento de um Microserviço de To-Do List
- Empresa: Montseguro
- Vaga: Desenvolvedor Back End Phyton Pleno
- Nome: José Dagmar Florentino da Silva Sobrinho

## Descrição

Repositório relacionado ao Desafio Técnico Backend do Montseguro Corretora

## Linguagens e Tecnologias utilizadas

- Python
- Banco de Dados SQLite e PostgreSQL
- IDE VSCode 
- Bibliotecas Python (fastapi, uvicorn, sqlalchemy)
- Docker

## Instruções para rodar o projeto

### 🔨 Guia de instalação

`git clone https://github.com/JulioSoaresA/desafio_tecnico_backend_montseguro.git`
`cd todo_list`

### Instalação de Ambiente Virtual
- Baixe esse repositório e entre no diretório do projeto
- Utilize um VirtualEnvironment<br>
`python -m venv venv`
- Ativando o ambiente virtual no linux<br>
`source venv/bin/activate`
- Ativando o ambiente virtual no windows<br>
`.\venv\Scripts\activate.ps1`
- Instale as dependências necessárias<br>
`pip install -r requirements.txt`

## Instruções para rodar o projeto localmente
`uvicorn app:app --reload `

## Instruções para rodar o projeto com Docker
`docker-compose up --build`
