FROM python:3.11-slim

# Spark 4 roda em Java 17/21 (Debian 13 traz o 21)
RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-21-jre-headless make \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app/src \
    LAKEHOUSE_ROOT=/app/lakehouse \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Padrão: roda testes + pipeline completo com a amostra.
# Dados reais: docker run ... anp-lakehouse make run gold SEMESTERS="2025-01"
CMD ["make", "all"]
