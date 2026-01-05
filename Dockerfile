FROM python:3.11-slim

# 1. Instala dependências de sistema necessárias para PDF e rede
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Copia e instala os requisitos primeiro (aproveita o cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copia o resto do código
COPY . .

# 4. Comando para rodar
CMD ["python", "main.py"]
