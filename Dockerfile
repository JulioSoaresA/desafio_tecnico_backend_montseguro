# Usando a imagem base do Python 3.10
FROM python:3.10-slim

# Instalando dependências do sistema e ferramentas de construção
RUN apt-get update \
    && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Definindo o diretório de trabalho
WORKDIR /app

# Copiando os arquivos de dependências e instalando as dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiando o restante do código da aplicação
COPY . .

# Expondo a porta que a aplicação irá utilizar
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
