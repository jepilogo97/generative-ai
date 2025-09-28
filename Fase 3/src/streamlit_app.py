import json
import re
from pathlib import Path
import tomli as tomllib
import streamlit as st
import ollama

# --- Configuración ---
settings_path = Path(__file__).resolve().parent / "settings.toml"
with settings_path.open("rb") as settings_file:
    SETTINGS = tomllib.load(settings_file)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
METADATA_FILE = DATA_DIR / "pedidos.json"

# Cargar todos los pedidos en memoria una sola vez
if "pedidos_data" not in st.session_state:
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        st.session_state.pedidos_data = json.load(f)


# --- Funciones auxiliares ---
def search_order(tracking_number: str) -> dict | None:
    """Busca un pedido exacto por número de seguimiento en la data ya cargada."""
    return next(
        (p for p in st.session_state.pedidos_data if p["tracking_number"] == tracking_number),
        None,
    )


def build_context(tracking_number: str) -> str:
    """
    Devuelve un texto descriptivo con toda la info del pedido,
    incluyendo productos, para que el modelo pueda responder
    tanto estado como devoluciones.
    """
    pedido = search_order(tracking_number)
    if not pedido:
        return f"No se encontró información para el pedido {tracking_number}."

    # Texto claro y amigable, no formato JSON
    detalles = []
    for k, v in pedido.items():
        if k == "productos":
            prod_txt = "; ".join(
                f"{p.get('nombre','')} ({p.get('categoria','')}, dev_aceptada: {p.get('dev_aceptada', False)})"
                for p in v
            )
            detalles.append(f"Productos: {prod_txt}")
        else:
            detalles.append(f"{k.replace('_',' ').capitalize()}: {v}")
    return "Información del pedido:\n" + "\n".join(detalles)


def assemble_messages(history: list[dict]) -> list[dict]:
    """
    Combina el historial de conversación del usuario con el role_prompt
    y las instrucciones para enviar a Ollama.
    """
    return [
        {"role": "system", "content": SETTINGS["prompts"]["role_prompt"]},
        {"role": "system", "content": SETTINGS["prompts"]["instruction_prompt"]},
    ] + history


def chat_with_ollama(messages: list[dict]) -> str:
    """
    Envía los mensajes acumulados a Ollama y devuelve la respuesta del asistente.
    Maneja posibles errores de conexión o de la API.
    """
    try:
        response = ollama.chat(
            model=SETTINGS["general"]["model"],
            messages=messages,
            options={"temperature": SETTINGS["general"].get("temperature", 0.7)},
        )
        return response["message"]["content"]
    except Exception as e:
        return f"Ocurrió un error al procesar la solicitud: {e}"


# --- Interfaz Streamlit tipo chat ---
st.title("💬 Asistente de Pedidos y Devoluciones de EcoMarket")

# Estado de la conversación
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Mostrar historial existente
for m in st.session_state.chat_history:
    with st.chat_message("user" if m["role"] == "user" else "assistant"):
        st.markdown(m["content"])

# Entrada del usuario
if user_input := st.chat_input("Pregunta..."):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    match = re.search(r"\b\d{5,}\b", user_input)
    if match and search_order(match.group()):
        context = build_context(match.group())
        st.session_state.chat_history.append({"role": "system", "content": context})

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            answer = chat_with_ollama(assemble_messages(st.session_state.chat_history))
            st.markdown(answer or "Sin respuesta")
    st.session_state.chat_history.append({"role": "assistant", "content": answer or "[sin respuesta]"})

# Render final del historial
for m in st.session_state.chat_history:
    with st.chat_message("user" if m["role"] == "user" else "assistant"):
        st.markdown(m["content"])