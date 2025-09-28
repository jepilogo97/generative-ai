# 📦 Sistema de Consulta de Pedidos con IA

Sistema de consulta de estado de pedidos que utiliza FAISS para búsqueda vectorial y Ollama (Llama 3) para generar respuestas inteligentes.

## 🚀 Inicio Rápido

### ⚡ Ejecución en 3 Pasos

1. **Abrir terminal** en el directorio `Fase 3/`
2. **Ejecutar script**: 
   - `python start.py` (Universal - Recomendado)
   - `bash start.sh` (Windows) o `./start.sh` (Linux/Mac)
3. **Abrir navegador** en: `http://localhost:8501`

> **⚠️ Primera vez**: La descarga del modelo puede tomar 10-15 minutos.

### Opción 1: Script Automático

#### 🐍 Python (Universal - Recomendado)
```bash
# Funciona en Windows, Linux, Mac, WSL
python start.py
```

#### 🐚 Bash Scripts
```bash
# Windows (PowerShell/CMD)
bash start.sh

# Linux/Mac
chmod +x start.sh
./start.sh

# WSL (si bash funciona)
bash start.sh
```


### Opción 2: Comandos Manuales
```bash
# 1. Verificar Docker
python check_docker.py

# 2. Construir imagen
docker build -t pedidos-app .

# 3. Ejecutar contenedor
docker run -p 8501:8501 -p 11434:11434 pedidos-app
```

### Acceder a la aplicación
Abre tu navegador en: `http://localhost:8501`

## 🎯 Uso

### Aplicación Web
Una vez que el contenedor esté ejecutándose, accede a:
- **URL**: `http://localhost:8501`
- **Funcionalidad**: Interfaz web para consultar estado de pedidos
- **Datos**: 24 pedidos de ejemplo disponibles

## 📁 Estructura del Proyecto

```
Fase 3/
├── src/
│   ├── app.py              # Script CLI principal
│   ├── streamlit_app.py    # Aplicación web
│   ├── ingest_data.py      # Creación de índice FAISS
│   └── settings.toml       # Configuración
├── data/
│   ├── pedidos.json        # Datos de pedidos
│   └── faiss_index.bin     # Índice FAISS (generado)
├── requirements.txt        # Dependencias
├── check_setup.py         # Script de verificación
└── README.md              # Este archivo
```

## 🔧 Solución de Problemas

#### Error: "Docker not found"
- **Causa**: Docker no instalado
- **Solución**: Instalar Docker Desktop desde https://www.docker.com/

#### Error: "Cannot connect to Docker daemon"
- **Causa**: Docker no está ejecutándose
- **Solución**: Iniciar Docker Desktop

#### Error: "Ollama not responding" en Docker
- **Causa**: Ollama no se inició correctamente en el contenedor
- **Solución**: Verificar logs con `docker logs <container_id>`

#### Error: "Model download failed" en Docker
- **Causa**: Problemas de red o espacio en disco
- **Solución**: Verificar conexión a internet y espacio disponible

#### Error: "Port already in use"
- **Causa**: Puerto 8501 o 11434 ya está en uso
- **Solución**: Cambiar puertos: `docker run -p 8502:8501 -p 11435:11434 pedidos-app`

#### Aplicación no carga
- **Causa**: Descarga del modelo aún en progreso
- **Solución**: Esperar 10-15 minutos y verificar logs: `docker logs <container_id>`

#### Error: "numpy.core.multiarray failed to import"
- **Causa**: Problema con la instalación de NumPy en el contenedor
- **Solución**: Reconstruir imagen sin caché: `docker build --no-cache -t pedidos-app .`

## 🤖 Modelos de IA

- **Embeddings**: `all-MiniLM-L6-v2` (Sentence Transformers)
- **LLM**: `llama3` (Ollama)
- **Búsqueda**: FAISS (Índice vectorial)


## 📋 Requisitos

- ✅ Docker Desktop instalado
- ✅ 4GB espacio libre
- ✅ Conexión a internet (primera vez)

## 🔧 Comandos Útiles

```bash
# Ver logs del contenedor
docker logs <container_id>

# Detener contenedor
docker stop <container_id>

# Eliminar imagen
docker rmi pedidos-app

# Ejecutar con volúmenes (persistir datos)
docker run -p 8501:8501 -p 11434:11434 -v ollama_data:/root/.ollama pedidos-app
```

## 📝 Notas

- **Docker**: El contenedor incluye todo lo necesario (Ollama + modelo + aplicación)
- **Primera ejecución**: La descarga del modelo llama3 puede tomar 10-15 minutos
- **Espacio requerido**: ~4GB para la imagen Docker completa
- **Puertos**: 8501 (Streamlit) y 11434 (Ollama)
- **Datos**: 30 pedidos de ejemplo incluidos

