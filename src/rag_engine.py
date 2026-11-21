import chromadb
from transformers import pipeline

from src.config import (
    MODEL_NAME,
    MAX_NEW_TOKENS,
    TOP_K,
    COLLECTION_NAME
)

# Conexión con ChromaDB

cliente = chromadb.PersistentClient(
    path="chroma_db"
)

coleccion = cliente.get_or_create_collection(
    name=COLLECTION_NAME
)

# Recuperación de contexto

def recuperar_contexto(pregunta):

    consulta = pregunta.upper()

    consulta = consulta.replace("¿QUÉ ES EL ", "")
    consulta = consulta.replace("¿QUE ES EL ", "")
    consulta = consulta.replace("¿QUÉ ES LA ", "")
    consulta = consulta.replace("¿QUE ES LA ", "")
    consulta = consulta.replace("?", "")
    consulta = consulta.strip()

    resultado = coleccion.query(
        query_texts=[consulta],
        n_results=TOP_K
    )

    contexto = resultado["documents"][0][0]

    return contexto

# Modelo de lenguaje

generador = pipeline(
    "text-generation",
    model=MODEL_NAME
)

SYSTEM_PROMPT = """
Eres SIN Assistant.

Eres un asistente especializado en el Sistema Interconectado Nacional (SIN) de Colombia y el Mercado de Energía Mayorista.

REGLAS OBLIGATORIAS:

1. Responde siempre en español.
2. Utiliza únicamente la información recuperada de la base de conocimiento.
3. No inventes información.
4. No uses conocimiento externo.
5. Si la información no aparece en el contexto recuperado, responde exactamente:

   "No encontré suficiente información en la base de conocimiento."

6. Explica los conceptos de forma clara para personas nuevas en la industria eléctrica.
7. Cuando exista una sigla, menciona primero el nombre completo y luego la sigla.
8. Sé breve y preciso.
"""

# Construcción del prompt RAG

def generar_prompt_rag(pregunta):

    contexto = recuperar_contexto(pregunta)

    prompt = f"""
{SYSTEM_PROMPT}

CONTEXTO RECUPERADO:

{contexto}

PREGUNTA DEL USUARIO:

{pregunta}

RESPUESTA BREVE Y PRECISA:
"""

    return prompt

# Generación de respuesta

def generar_respuesta(pregunta):

    contexto = recuperar_contexto(pregunta)

    return contexto
