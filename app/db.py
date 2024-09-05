from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conectando ao banco de dados PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/todo_list"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Configuração da base para os modelos
Base = declarative_base()

# Criação das tabelas
Base.metadata.create_all(bind=engine)

# Sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
