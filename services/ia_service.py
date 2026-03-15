import streamlit as st
from groq import Groq
import json
from services.search_service import buscar_info


@st.cache_resource
def get_groq():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])


def consultar_ia(nombre: str, partido: str, pregunta: str, contexto: str) -> str:
    groq = get_groq()
    prompt = f"""Eres un asistente político neutral e informativo para ciudadanos peruanos.
Candidato: {nombre} — {partido}

INFORMACIÓN WEB ACTUALIZADA:
{contexto}

PREGUNTA: {pregunta}

Responde de forma clara, objetiva y sin favorecer ni atacar al candidato.
Menciona la fuente si es información verificada. Máximo 3 párrafos en español."""

    mensaje = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    return mensaje.choices[0].message.content


@st.cache_data(ttl=1800)
def cargar_perfil(nombre: str, partido: str) -> dict:
    contexto, _ = buscar_info(
        f"{nombre} candidato presidencial Peru 2026 perfil biografia "
        f"trayectoria propuestas denuncias antecedentes partido {partido}"
    )
    groq = get_groq()
    prompt = f"""Analiza la siguiente información sobre el candidato presidencial peruano {nombre}
del partido {partido} para las elecciones 2026.

INFORMACIÓN:
{contexto}

Devuelve SOLO un JSON puro sin markdown con este formato exacto:
{{
  "edad": "edad o rango aproximado",
  "profesion": "profesión principal",
  "trayectoria": "2-3 oraciones sobre su carrera política",
  "propuestas_clave": ["propuesta 1", "propuesta 2", "propuesta 3"],
  "alertas": ["denuncia o escándalo 1", "denuncia 2"],
  "puntos_positivos": ["logro o punto positivo 1", "logro 2"],
  "posicion_ideologica": "izquierda / centro-izquierda / centro / centro-derecha / derecha",
  "frase_clave": "una frase o propuesta destacada del candidato"
}}

Si no tienes información sobre algún campo usa "No disponible".
Solo incluye alertas reales con fuentes, no inventes denuncias."""

    mensaje = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = mensaje.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    try:
        return json.loads(raw)
    except Exception:
        return {}
