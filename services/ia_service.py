# Importamos las librerías necesarias
import streamlit as st      # Para cache y secrets
from groq import Groq       # Cliente de Groq (IA gratuita)
import json                 # Para manejar datos en formato JSON

# Importamos la función de búsqueda web del otro servicio
from services.search_service import buscar_info


# ── Conexion con Groq ────────────────────────────────────────────
# @st.cache_resource significa que Groq se conecta UNA sola vez
# y se reutiliza en todas las consultas — evita reconectarse cada vez
@st.cache_resource
def get_groq():
    # Lee la API Key desde .streamlit/secrets.toml de forma segura
    # Nunca escribimos la clave directo en el código
    return Groq(api_key=st.secrets["GROQ_API_KEY"])


# ── Consulta libre al candidato ──────────────────────────────────
# Esta función recibe la pregunta del usuario y devuelve la respuesta de la IA
def consultar_ia(nombre: str, partido: str, pregunta: str, contexto: str) -> str:

    # Obtenemos el cliente de Groq (ya conectado)
    groq = get_groq()

    # El prompt es el mensaje que le enviamos a la IA
    # Le damos contexto, rol y reglas claras de comportamiento
    prompt = f"""Eres un asistente político neutral e informativo para ciudadanos peruanos.
Candidato: {nombre} — {partido}

INFORMACIÓN WEB ACTUALIZADA:
{contexto}

PREGUNTA: {pregunta}

Responde de forma clara, objetiva y sin favorecer ni atacar al candidato.
Menciona la fuente si es información verificada. Máximo 3 párrafos en español."""

    # Enviamos el mensaje a la IA y esperamos la respuesta
    # model: el modelo de IA que usamos (LLaMA 3.3 de Meta, gratis en Groq)
    # max_tokens: máximo de palabras que puede responder
    # messages: el historial de la conversación (solo enviamos 1 mensaje)
    mensaje = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )

    # Extraemos el texto de la respuesta y lo devolvemos
    # choices[0] = primera respuesta (solo pedimos una)
    # message.content = el texto en sí
    return mensaje.choices[0].message.content


# ── Perfil completo del candidato ────────────────────────────────
# @st.cache_data(ttl=1800) guarda el resultado en memoria por 30 minutos
# Si alguien consulta el mismo candidato dos veces, no gasta búsquedas
# ttl = "time to live" = tiempo de vida del cache en segundos
@st.cache_data(ttl=1800)
def cargar_perfil(nombre: str, partido: str) -> dict:

    # Primero buscamos información real en internet sobre el candidato
    # Combinamos varios temas en una sola búsqueda para obtener más datos
    contexto, _ = buscar_info(
        f"{nombre} candidato presidencial Peru 2026 perfil biografia "
        f"trayectoria propuestas denuncias antecedentes partido {partido}"
    )

    # Obtenemos el cliente de Groq
    groq = get_groq()

    # Le pedimos a la IA que analice lo que encontró y lo organice en JSON
    # JSON es un formato de datos estructurado — como un diccionario de Python
    # Le damos el formato EXACTO que queremos para poder procesarlo después
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

Reglas importantes:
- propuestas_clave, alertas y puntos_positivos SIEMPRE deben ser listas de strings completos
- Cada elemento de la lista debe ser una frase completa, nunca letras sueltas
- Si no tienes información sobre algún campo usa "No disponible"
- Solo incluye alertas reales con fuentes, no inventes denuncias"""

    # Enviamos el prompt a la IA
    mensaje = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )

    # Obtenemos el texto de la respuesta
    raw = mensaje.choices[0].message.content.strip()

    # A veces la IA devuelve el JSON dentro de bloques de código markdown
    # como ```json ... ``` — lo limpiamos para quedarnos solo con el JSON puro
    if raw.startswith("```"):
        # Separamos por ``` y tomamos la segunda parte (el contenido)
        raw = raw.split("```")[1]
        # Si empieza con "json" lo removemos (es solo una etiqueta)
        if raw.startswith("json"):
            raw = raw[4:]

    # Intentamos convertir el texto JSON a un diccionario de Python
    try:
        datos = json.loads(raw)

        # Verificamos que los campos de lista sean realmente listas válidas
        # A veces la IA devuelve un string en lugar de una lista
        for campo in ["propuestas_clave", "alertas", "puntos_positivos"]:

            # Obtenemos el valor del campo, si no existe usamos lista vacía
            valor = datos.get(campo, [])

            # Caso 1: la IA devolvió un string en lugar de lista
            # Ejemplo: "propuesta1, propuesta2" en vez de ["propuesta1", "propuesta2"]
            # Lo dividimos por comas y limpiamos espacios
            if isinstance(valor, str):
                datos[campo] = [v.strip()
                                for v in valor.split(",") if v.strip()]

            # Caso 2: la IA devolvió una lista pero con letras sueltas
            # Ejemplo: ["N", "o", " ", "d"] en vez de ["No disponible"]
            # isinstance(valor, list) verifica que sea una lista
            # any(...) verifica si ALGÚN elemento tiene 2 caracteres o menos
            elif isinstance(valor, list) and any(len(str(v)) <= 2 for v in valor):
                datos[campo] = ["No disponible"]

        # Devolvemos el diccionario limpio y validado
        return datos

    # Si json.loads falla (el texto no es JSON válido) devolvemos diccionario vacío
    # Esto evita que la app se rompa — muestra "N/D" en lugar de un error
    except Exception:
        return {}
