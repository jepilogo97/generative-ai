# ============================================================
# Imagen base
# ============================================================
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV PATH="/root/.local/bin:${PATH}"

# ------------------------------------------------------------
# 1. Paquetes del sistema
# ------------------------------------------------------------
RUN apt-get update && apt-get install -y \
    curl wget build-essential \
    gcc g++ gfortran \
    libopenblas-dev liblapack-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# 2. Instalar Ollama
# ------------------------------------------------------------
RUN curl -fsSL https://ollama.com/install.sh | sh

# Configurar Ollama
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_ORIGINS=*

# ------------------------------------------------------------
# 3. Entorno Python
# ------------------------------------------------------------
WORKDIR /app
COPY requirements.txt .

# Instalar dependencias en orden específico para evitar conflictos
RUN pip install --no-cache-dir --upgrade pip

# Instalar NumPy primero con dependencias específicas
RUN pip install --no-cache-dir numpy==1.24.4

# Instalar el resto de dependencias
RUN pip install --no-cache-dir -r requirements.txt

# ------------------------------------------------------------
# 4. Copiar el proyecto y el entrypoint
# ------------------------------------------------------------
COPY . .
RUN chmod +x /app/entrypoint.sh

# Crear directorio para datos de Ollama
RUN mkdir -p /root/.ollama

# ------------------------------------------------------------
# 5. Puertos expuestos
# ------------------------------------------------------------
# Puertos expuestos
EXPOSE 8501
EXPOSE 11434

# ------------------------------------------------------------
# 6. Comando de arranque
# ------------------------------------------------------------
CMD ["/app/entrypoint.sh"]
