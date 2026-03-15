import streamlit as st
from groq import Groq
from tavily import TavilyClient
import json

# ── Configuracion de pagina ──────────────────────────────────────
st.set_page_config(
    page_title="Candidatos Perú 2026",
    page_icon="🇵🇪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Estilos ──────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .header-box {
        background: linear-gradient(135deg, #C8102E, #D4AF37);
        padding: 2rem; border-radius: 16px;
        text-align: center; margin-bottom: 1.5rem;
    }
    .header-box h1 { color: white; font-size: clamp(1.4rem, 4vw, 2.2rem); margin: 0; }
    .header-box p  { color: rgba(255,255,255,0.85); margin: 0.5rem 0 0;
                     font-size: clamp(0.8rem, 2vw, 1rem); }

    .perfil-card {
        background: #fff;
        border-radius: 16px;
        padding: 1.5rem;
        border: 2px solid #e9ecef;
        margin-bottom: 1rem;
    }
    .perfil-nombre { color: #C8102E; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.2rem; }
    .perfil-partido { color: #6c757d; font-size: 0.85rem; margin-bottom: 1rem; }
    .perfil-dato { font-size: 0.85rem; margin-bottom: 0.4rem; color: #343a40; }
    .perfil-dato strong { color: #C8102E; }

    .badge-alerta {
        background: #fff3cd; border: 1px solid #ffc107;
        border-radius: 8px; padding: 0.35rem 0.75rem;
        font-size: 0.78rem; color: #856404;
        display: inline-block; margin: 0.2rem;
    }
    .badge-ok {
        background: #d1e7dd; border: 1px solid #198754;
        border-radius: 8px; padding: 0.35rem 0.75rem;
        font-size: 0.78rem; color: #0f5132;
        display: inline-block; margin: 0.2rem;
    }
    .badge-info {
        background: #cff4fc; border: 1px solid #0dcaf0;
        border-radius: 8px; padding: 0.35rem 0.75rem;
        font-size: 0.78rem; color: #055160;
        display: inline-block; margin: 0.2rem;
    }

    .respuesta-box {
        background: #f0f4ff;
        border-left: 4px solid #C8102E;
        border-radius: 0 12px 12px 0;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
        font-size: 0.92rem;
        line-height: 1.7;
    }

    .encuesta-box {
        background: #fff8e1;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        border: 1px solid #ffe082;
        margin-bottom: 1rem;
        font-size: 0.85rem;
    }

    .stButton > button {
        background: #C8102E !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        width: 100%;
    }
    .stButton > button:hover { background: #a00d24 !important; }
    footer { visibility: hidden; }

    @media (max-width: 640px) {
        .header-box { padding: 1.2rem; }
        .perfil-card { padding: 1rem; }
    }
</style>
""", unsafe_allow_html=True)

# ── Clientes ─────────────────────────────────────────────────────


@st.cache_resource
def get_clients():
    groq_c = Groq(api_key=st.secrets["GROQ_API_KEY"])
    tavily = TavilyClient(api_key=st.secrets["TAVILY_API_KEY"])
    return groq_c, tavily


groq_client, tavily_client = get_clients()

# ── Candidatos oficiales Peru 2026 ───────────────────────────────
CANDIDATOS = {
    "Selecciona un candidato...": None,
    "Keiko Fujimori — Fuerza Popular": {"nombre": "Keiko Fujimori", "partido": "Fuerza Popular"},
    "Rafael López Aliaga — Renovación Popular": {"nombre": "Rafael López Aliaga", "partido": "Renovación Popular"},
    "César Acuña — Alianza para el Progreso": {"nombre": "César Acuña", "partido": "Alianza para el Progreso"},
    "George Forsyth — Somos Perú": {"nombre": "George Forsyth", "partido": "Somos Perú"},
    "José Williams — Avanza País": {"nombre": "José Williams", "partido": "Avanza País"},
    "Alfonso López Chau — Ahora Nación": {"nombre": "Alfonso López Chau", "partido": "Ahora Nación"},
    "Alfredo Barnechea — Acción Popular": {"nombre": "Alfredo Barnechea", "partido": "Acción Popular"},
    "Yonhy Lescano — Cooperación Popular": {"nombre": "Yonhy Lescano", "partido": "Cooperación Popular"},
    "Roberto Sánchez — Juntos por el Perú": {"nombre": "Roberto Sánchez", "partido": "Juntos por el Perú"},
    "Mesías Guevara — Partido Morado": {"nombre": "Mesías Guevara", "partido": "Partido Morado"},
    "Marisol Pérez Tello — Primero la Gente": {"nombre": "Marisol Pérez Tello", "partido": "Primero la Gente"},
    "Fernando Olivera — Frente de la Esperanza 2021": {"nombre": "Fernando Olivera", "partido": "Frente de la Esperanza 2021"},
    "Vladimir Cerrón — Perú Libre": {"nombre": "Vladimir Cerrón", "partido": "Perú Libre"},
    "José Luna Gálvez — Podemos Perú": {"nombre": "José Luna Gálvez", "partido": "Podemos Perú"},
    "Mario Vizcarra — Perú Primero": {"nombre": "Mario Vizcarra", "partido": "Perú Primero"},
    "Álvaro Paz de la Barra — Fe en el Perú": {"nombre": "Álvaro Paz de la Barra", "partido": "Fe en el Perú"},
    "Fiorella Molinelli — Fuerza y Libertad": {"nombre": "Fiorella Molinelli", "partido": "Fuerza y Libertad"},
    "Jorge Nieto — Partido del Buen Gobierno": {"nombre": "Jorge Nieto", "partido": "Partido del Buen Gobierno"},
    "Rosario Fernández — Un Camino Diferente": {"nombre": "Rosario Fernández", "partido": "Un Camino Diferente"},
    "Walter Chirinos — PRIN": {"nombre": "Walter Chirinos", "partido": "PRIN"},
    "Ricardo Belmont — Obras": {"nombre": "Ricardo Belmont", "partido": "Obras"},
    "Carlos Álvarez — País Para Todos": {"nombre": "Carlos Álvarez", "partido": "País Para Todos"},
    "Paul Jaimes — Progresemos": {"nombre": "Paul Jaimes", "partido": "Progresemos"},
    "Carlos Espá — Sí Creo": {"nombre": "Carlos Espá", "partido": "Sí Creo"},
    "Ronald Atencio — Venceremos": {"nombre": "Ronald Atencio", "partido": "Venceremos"},
    "Antonio Ortiz — Salvemos al Perú": {"nombre": "Antonio Ortiz", "partido": "Salvemos al Perú"},
    "Herbert Caller — Partido Patriótico del Perú": {"nombre": "Herbert Caller", "partido": "Partido Patriótico del Perú"},
    "Charlie Carrasco — Partido Demócrata Unido": {"nombre": "Charlie Carrasco", "partido": "Partido Demócrata Unido"},
    "Armando Massé — Partido Democrático Federal": {"nombre": "Armando Massé", "partido": "Partido Democrático Federal"},
    "Wolfgang Grozo — Integridad Democrática": {"nombre": "Wolfgang Grozo", "partido": "Integridad Democrática"},
    "Carlos Jaico — Perú Moderno": {"nombre": "Carlos Jaico", "partido": "Perú Moderno"},
    "Rafael Belaunde — Libertad Popular": {"nombre": "Rafael Belaunde", "partido": "Libertad Popular"},
    "Roberto Chiabra — Unidad Nacional": {"nombre": "Roberto Chiabra", "partido": "Unidad Nacional"},
    "Napoleón Becerra — Trabajadores y Emprendedores": {"nombre": "Napoleón Becerra", "partido": "Trabajadores y Emprendedores"},
    "Alex Gonzales — Partido Demócrata Verde": {"nombre": "Alex Gonzales", "partido": "Partido Demócrata Verde"},
    "Francisco Diez Canseco — Perú Acción": {"nombre": "Francisco Diez Canseco", "partido": "Perú Acción"},
}

# ── Buscar info con Tavily ───────────────────────────────────────


def buscar_info(query: str):
    try:
        resultado = tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=6,
            include_answer=True
        )
        textos, fuentes = [], []
        if resultado.get("answer"):
            textos.append(resultado["answer"])
        for r in resultado.get("results", []):
            textos.append(f"- {r['title']}: {r['content'][:400]}")
            fuentes.append(f"• [{r['title']}]({r.get('url', '')})")
        return "\n".join(textos), fuentes
    except Exception as e:
        return f"Error: {e}", []

# ── Cargar perfil completo del candidato ─────────────────────────


@st.cache_data(ttl=1800)
def cargar_perfil(nombre: str, partido: str) -> dict:
    contexto, _ = buscar_info(
        f"{nombre} candidato presidencial Peru 2026 perfil biografia "
        f"trayectoria propuestas denuncias antecedentes partido {partido}"
    )
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

Si no tienes información sobre algún campo, usa "No disponible".
Solo incluye alertas reales con fuentes, no inventes denuncias."""

    mensaje = groq_client.chat.completions.create(
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

# ── Consultar IA ─────────────────────────────────────────────────


def consultar_ia(nombre: str, partido: str, pregunta: str, contexto: str) -> str:
    prompt = f"""Eres un asistente político neutral e informativo para ciudadanos peruanos.
Candidato: {nombre} — {partido}

INFORMACIÓN WEB ACTUALIZADA:
{contexto}

PREGUNTA: {pregunta}

Responde de forma clara, objetiva y sin favorecer ni atacar al candidato.
Menciona la fuente si es información verificada. Máximo 3 párrafos en español."""

    mensaje = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    return mensaje.choices[0].message.content

# ── Renderizar perfil visual ─────────────────────────────────────


def mostrar_perfil(candidato: dict, perfil: dict):
    nombre = candidato["nombre"]
    partido = candidato["partido"]

    ideologia = perfil.get("posicion_ideologica", "No disponible")
    color_ideo = {
        "izquierda": "#dc3545", "centro-izquierda": "#fd7e14",
        "centro": "#6c757d", "centro-derecha": "#0d6efd", "derecha": "#0a58ca"
    }.get(ideologia.lower(), "#6c757d")

    st.markdown(f"""
    <div class="perfil-card">
        <div class="perfil-nombre">{nombre}</div>
        <div class="perfil-partido">🏛 {partido}</div>
        <div class="perfil-dato"><strong>Edad:</strong> {perfil.get('edad', 'N/D')}</div>
        <div class="perfil-dato"><strong>Profesión:</strong> {perfil.get('profesion', 'N/D')}</div>
        <div class="perfil-dato"><strong>Posición:</strong>
            <span style="color:{color_ideo}; font-weight:600;">{ideologia}</span>
        </div>
        <div class="perfil-dato" style="margin-top:0.8rem;">
            <strong>Trayectoria:</strong><br>{perfil.get('trayectoria', 'N/D')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    frase = perfil.get("frase_clave", "")
    if frase and frase != "No disponible":
        st.markdown(f"""
        <div style="background:#f8f9fa; border-left:4px solid #D4AF37;
                    border-radius:0 8px 8px 0; padding:0.8rem 1rem;
                    font-style:italic; color:#495057; margin-bottom:1rem;">
            "{frase}"
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Propuestas clave:**")
        for p in perfil.get("propuestas_clave", []):
            if p and p != "No disponible":
                st.markdown(f'<span class="badge-info">📋 {p}</span>',
                            unsafe_allow_html=True)
    with col2:
        alertas = [a for a in perfil.get(
            "alertas", []) if a and a != "No disponible"]
        positivos = [p for p in perfil.get(
            "puntos_positivos", []) if p and p != "No disponible"]
        if alertas:
            st.markdown("**Alertas y denuncias:**")
            for a in alertas:
                st.markdown(f'<span class="badge-alerta">⚠ {a}</span>',
                            unsafe_allow_html=True)
        if positivos:
            st.markdown("**Puntos destacables:**")
            for p in positivos:
                st.markdown(f'<span class="badge-ok">✓ {p}</span>',
                            unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  INTERFAZ PRINCIPAL
# ════════════════════════════════════════════════════════════════


st.markdown("""
<div class="header-box">
    <h1>🇵🇪 Comparador de Candidatos Peru 2026</h1>
    <p>36 candidatos oficiales · Perfiles en tiempo real · Elecciones 12 de abril 2026</p>
</div>
""", unsafe_allow_html=True)

st.success(
    f"✅ {len(CANDIDATOS) - 1} candidatos oficiales inscritos ante el JNE")

tab1, tab2 = st.tabs(["🔍 Perfil y consulta", "⚖️ Comparar candidatos"])

# ══════════════════════════════
#  TAB 1 — Perfil + consulta
# ══════════════════════════════
with tab1:
    candidato_key = st.selectbox(
        "Selecciona un candidato",
        options=list(CANDIDATOS.keys()),
        key="sel_individual"
    )

    if CANDIDATOS[candidato_key]:
        candidato = CANDIDATOS[candidato_key]

        with st.spinner(f"Cargando perfil de {candidato['nombre']}..."):
            perfil = cargar_perfil(candidato["nombre"], candidato["partido"])

        if perfil:
            mostrar_perfil(candidato, perfil)
        else:
            st.warning("No se pudo cargar el perfil completo.")

        st.markdown("---")
        st.markdown("#### Hazle una pregunta")

        preguntas_rapidas = [
            "¿Tiene denuncias penales o sentencias?",
            "¿Cuáles son sus propuestas principales?",
            "¿Qué escándalos tiene?",
            "¿Cuál es su propuesta económica?",
            "¿Qué propone para la seguridad ciudadana?",
            "¿Qué propone para la educación y salud?",
            "¿Tiene inhabilitaciones vigentes?",
        ]

        col_q1, col_q2 = st.columns([2, 1])
        with col_q1:
            pregunta_rapida = st.selectbox(
                "Preguntas frecuentes",
                ["Escribe tu propia pregunta..."] + preguntas_rapidas,
                key="rapidas"
            )
            if pregunta_rapida == "Escribe tu propia pregunta...":
                pregunta = st.text_input(
                    "Tu pregunta",
                    placeholder="Ej: ¿Qué propone para reducir la pobreza?",
                    key="pregunta_libre"
                )
            else:
                pregunta = pregunta_rapida

        with col_q2:
            st.markdown("<br>", unsafe_allow_html=True)
            consultar = st.button("Consultar", key="btn_consultar")

        if consultar and pregunta:
            with st.spinner("Buscando en internet..."):
                query = f"{candidato['nombre']} {pregunta} Peru 2026"
                contexto, fuentes = buscar_info(query)
                respuesta = consultar_ia(
                    candidato["nombre"], candidato["partido"], pregunta, contexto
                )
                st.markdown(
                    f'<div class="respuesta-box">{respuesta}</div>',
                    unsafe_allow_html=True
                )
                if fuentes:
                    with st.expander("Ver fuentes consultadas"):
                        for f in fuentes:
                            st.markdown(f)

# ══════════════════════════════
#  TAB 2 — Comparacion
# ══════════════════════════════
with tab2:
    st.markdown("### Compara dos candidatos lado a lado")

    opciones = [k for k in CANDIDATOS.keys() if CANDIDATOS[k] is not None]

    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        key_a = st.selectbox("Candidato A", opciones, key="comp_a")
    with col_b:
        key_b = st.selectbox(
            "Candidato B", opciones,
            index=1 if len(opciones) > 1 else 0,
            key="comp_b"
        )

    tema_comparacion = st.selectbox(
        "Tema a comparar",
        ["Propuestas económicas", "Seguridad y justicia",
         "Educación y salud", "Antecedentes y denuncias",
         "Medio ambiente", "Corrupción",
         "Empleo y economía", "Política exterior"]
    )

    if st.button("Comparar ahora", key="btn_comparar"):
        if key_a == key_b:
            st.warning("Selecciona dos candidatos diferentes.")
        else:
            cand_a = CANDIDATOS[key_a]
            cand_b = CANDIDATOS[key_b]
            col_res_a, col_res_b = st.columns(2, gap="large")

            for col, cand in [(col_res_a, cand_a), (col_res_b, cand_b)]:
                with col:
                    with st.spinner(f"Analizando a {cand['nombre']}..."):
                        perfil = cargar_perfil(cand["nombre"], cand["partido"])
                        if perfil:
                            mostrar_perfil(cand, perfil)
                        query = f"{cand['nombre']} {tema_comparacion} Peru 2026"
                        contexto, fuentes = buscar_info(query)
                        pregunta = f"¿Cuál es la posición de este candidato respecto a: {tema_comparacion}?"
                        respuesta = consultar_ia(
                            cand["nombre"], cand["partido"], pregunta, contexto
                        )
                        st.markdown(
                            f'<div class="respuesta-box">{respuesta}</div>',
                            unsafe_allow_html=True
                        )
                        if fuentes:
                            with st.expander("Ver fuentes"):
                                for f in fuentes:
                                    st.markdown(f)

# ── Footer ───────────────────────────────────────────────────────
# ── Footer ───────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding: 1rem 0;">
    <p style="color:#6c757d; font-size:0.78rem; margin-bottom:0.8rem;">
        Información de fuentes públicas y búsqueda web en tiempo real.<br>
        Proyecto educativo y apartidario · Verifica siempre en fuentes oficiales:
        <a href="https://infogob.jne.gob.pe" target="_blank">JNE</a> ·
        <a href="https://www.onpe.gob.pe" target="_blank">ONPE</a>
    </p>
    <div style="background: linear-gradient(135deg, #0D1B2A, #1A3A5C);
                border-radius: 12px; padding: 1rem 1.5rem;
                display: inline-block; margin: 0 auto;">
        <p style="color:rgba(255,255,255,0.6); font-size:0.72rem;
                  letter-spacing:2px; text-transform:uppercase; margin:0 0 0.4rem;">
            Desarrollado por
        </p>
        <p style="color:white; font-size:1rem; font-weight:700; margin:0 0 0.3rem;">
            Alexander Guevara
        </p>
        <p style="color:rgba(255,255,255,0.5); font-size:0.75rem; margin:0;">
            🇵🇪 Lima, Perú · 2026
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
