#!/usr/bin/env python3
"""
Script de inicio universal para Docker (Python)
Funciona en Windows, Linux, Mac y WSL
"""

import subprocess
import sys
import os

def run_command(cmd, description=""):
    """Ejecuta un comando y maneja errores."""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - OK")
            return True
        else:
            print(f"❌ {description} - ERROR: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - EXCEPCIÓN: {e}")
        return False

def check_docker():
    """Verifica que Docker esté instalado y ejecutándose."""
    print("🐳 Verificando Docker...")
    
    # Verificar que Docker esté instalado
    if not run_command("docker --version", "Verificando instalación de Docker"):
        print("❌ Docker no está instalado")
        print("💡 Descarga Docker Desktop desde: https://www.docker.com/")
        return False
    
    # Verificar que Docker esté ejecutándose
    if not run_command("docker info", "Verificando que Docker esté ejecutándose"):
        print("❌ Docker no está ejecutándose")
        print("💡 Inicia Docker Desktop")
        return False
    
    print("✅ Docker verificado")
    return True

def build_image(force_rebuild=False):
    """Construye la imagen Docker si no existe."""
    print("🔍 Verificando imagen Docker...")
    
    # Verificar si la imagen existe
    result = subprocess.run("docker image inspect pedidos-app", 
                           shell=True, capture_output=True, text=True)
    
    if result.returncode == 0 and not force_rebuild:
        print("✅ Imagen ya existe")
        return True
    
    if force_rebuild:
        print("🔨 Reconstruyendo imagen Docker (sin caché)...")
        print("⚠️  Esto puede tomar 10-15 minutos")
        cmd = "docker build --no-cache -t pedidos-app ."
    else:
        print("🔨 Construyendo imagen Docker...")
        print("⚠️  Esto puede tomar 10-15 minutos en la primera vez")
        cmd = "docker build -t pedidos-app ."
    
    if run_command(cmd, "Construyendo imagen"):
        print("✅ Imagen construida exitosamente")
        return True
    else:
        print("❌ Error construyendo imagen")
        return False

def run_container():
    """Ejecuta el contenedor Docker."""
    print("🚀 Iniciando contenedor...")
    print("📱 La aplicación estará disponible en: http://localhost:8501")
    print("⏳ Esperando a que Ollama descargue el modelo (puede tomar varios minutos)...")
    print("")
    
    # Verificar si hay contenedores ejecutándose
    result = subprocess.run("docker ps --filter name=pedidos-app", 
                           shell=True, capture_output=True, text=True)
    
    if "pedidos-app" in result.stdout:
        print("⚠️  Ya hay un contenedor ejecutándose")
        print("💡 Detén el contenedor anterior con: docker stop $(docker ps -q --filter ancestor=pedidos-app)")
        return False
    
    # Ejecutar contenedor
    try:
        subprocess.run("docker run -p 8501:8501 -p 11434:11434 pedidos-app", 
                      shell=True, check=True)
    except subprocess.CalledProcessError as e:
        error_msg = str(e)
        if "port is already allocated" in error_msg:
            print("❌ Puerto 8501 ya está en uso")
            print("💡 Detén otros contenedores o cambia el puerto:")
            print("   docker run -p 8502:8501 -p 11435:11434 pedidos-app")
        elif "numpy.core.multiarray" in error_msg:
            print("❌ Error con NumPy en el contenedor")
            print("💡 Reconstruye la imagen con:")
            print("   docker build --no-cache -t pedidos-app .")
        else:
            print(f"❌ Error ejecutando contenedor: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Contenedor detenido por el usuario")
        return True
    
    return True

def main():
    """Función principal."""
    print("🚀 Iniciando Sistema de Consulta de Pedidos con IA")
    print("==================================================")
    print("")
    
    # Verificar Docker
    if not check_docker():
        return 1
    
    # Construir imagen
    if not build_image():
        return 1
    
    # Ejecutar contenedor
    if not run_container():
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
