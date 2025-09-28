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
    Devuelve un texto descriptivo con la info del pedido
    para que el modelo responda (no se mostrará en la interfaz).
    """
    pedido = search_order(tracking_number)
    if not pedido:
        return f"No se encontró información para el pedido {tracking_number}."

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

def assemble_messages(history: list[dict], extra_system: str | None = None) -> list[dict]:
    """
    Combina prompts fijos + historial del usuario, opcionalmente
    añade un contexto extra solo para el modelo.
    """
    base = [
        {"role": "system", "content": SETTINGS["prompts"]["role_prompt"]},
        {"role": "system", "content": SETTINGS["prompts"]["instruction_prompt"]},
    ]
    if extra_system:
        base.append({"role": "system", "content": extra_system})
    return base + history

def chat_with_ollama(messages: list[dict]) -> str:
    """Envía los mensajes a Ollama y devuelve la respuesta."""
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

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if user_input := st.chat_input("Pregunta..."):
    # guardar y mostrar mensaje del usuario
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # detectar tracking y preparar contexto SOLO para el modelo
    context = None
    match = re.search(r"\b\d{5,}\b", user_input)
    if match and search_order(match.group()):
        context = build_context(match.group())

    # obtener respuesta del modelo
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            answer = chat_with_ollama(
                assemble_messages(st.session_state.chat_history, extra_system=context)
            )
            st.markdown(answer or "Sin respuesta")

    # guardar respuesta en el historial (solo texto del bot)
    st.session_state.chat_history.append({"role": "assistant", "content": answer or "[sin respuesta]"})

# --- Render único del historial (solo user/assistant) ---
for m in st.session_state.chat_history:
    with st.chat_message("user" if m["role"] == "user" else "assistant"):
        st.markdown(m["content"])
