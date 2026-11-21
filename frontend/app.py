import streamlit as st

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.rag_engine import generar_respuesta

st.set_page_config(
    page_title="SIN Assistant",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ SIN Assistant")

st.write(
    """
    Asistente especializado en el Sistema Interconectado Nacional de Colombia.

    Puede consultar conceptos técnicos del glosario XM.
    """
)

# Memoria conversacional de corto plazo

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar historial

for mensaje in st.session_state.mensajes:

    with st.chat_message(mensaje["rol"]):
        st.markdown(mensaje["contenido"])

# Entrada del usuario

pregunta = st.chat_input(
    "Escriba su pregunta..."
)

if pregunta:

    st.session_state.mensajes.append(
        {
            "rol": "user",
            "contenido": pregunta
        }
    )

    with st.chat_message("user"):
        st.markdown(pregunta)

    respuesta = generar_respuesta(
        pregunta
    )

    st.session_state.mensajes.append(
        {
            "rol": "assistant",
            "contenido": respuesta
        }
    )

    with st.chat_message("assistant"):
        st.markdown(respuesta)