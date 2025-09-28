#!/bin/bash
set -e

echo "🚀 Iniciando Ollama..."
ollama serve &
OLLAMA_PID=$!

# Esperar a que Ollama esté listo
echo "⏳ Esperando a que Ollama esté listo..."
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✅ Ollama está listo"
        break
    fi
    echo "   Intento $i/30..."
    sleep 2
done

echo "⬇️  Descargando modelo llama3 (solo si no existe)..."
ollama pull llama3 || echo "⚠️  No se pudo descargar llama3, continuando..."

echo "🔍 Verificando que el modelo esté disponible..."
if ollama list | grep -q "llama3"; then
    echo "✅ Modelo llama3 disponible"
else
    echo "⚠️  Modelo llama3 no encontrado, pero continuando..."
fi

echo "✅ Lanzando aplicación Streamlit..."
streamlit run src/streamlit_app.py --server.port=8501 --server.address=0.0.0.0