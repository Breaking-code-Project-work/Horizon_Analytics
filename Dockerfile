FROM python:3.12-slim

WORKDIR /app

# installa bash, librerie PostgreSQL e gcc
RUN apt-get update && apt-get install -y \
    bash \
    libpq-dev \
    gcc \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# copia requirements e installa
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copia il resto del progetto
COPY . .

# rendi start.sh eseguibile dentro il container
RUN chmod +x start.sh

EXPOSE 8000

# usa bash per eseguire start.sh
CMD ["bash", "start.sh"]
