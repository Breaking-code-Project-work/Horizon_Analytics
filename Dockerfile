FROM python:3.12-slim

WORKDIR /app

# installa bash, librerie PostgreSQL, gcc e git
RUN apt-get update && apt-get install -y \
    libpq-dev gcc postgresql-client bash git \
    && apt-get clean

# copia requirements e installa
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copia il resto del progetto
COPY . .

# rendi start.sh eseguibile dentro il container
RUN chmod +x start.sh

EXPOSE 8000

CMD ["/bin/bash", "/app/start.sh"]