import streamlit as st
from config.candidatos import CANDIDATOS
from services.ia_service import cargar_perfil, consultar_ia
from services.search_service import buscar_info
from components.perfil_card import mostrar_perfil

# ── Configuracion ────────────────────────────────────────────────
st.set_page_config(
    page_title="Candidatos Perú 2026",
    page_icon="🇵🇪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Estilos ──────────────────────────────────────────────────────
with open("styles/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Limite de consultas por sesion ───────────────────────────────
if "consultas" not in st.session_state:
    st.session_state.consultas = 0


def verificar_limite():
    if st.session_state.consultas >= 10:
        st.warning(
            "Alcanzaste el límite de 10 consultas por sesión. Recarga la página para continuar.")
        st.stop()
    st.session_state.consultas += 1


# ── Header ───────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <h1>🇵🇪 Candidatos Peru 2026</h1>
    <p>36 candidatos oficiales · Perfiles en tiempo real · Elecciones 12 de abril 2026</p>
</div>
""", unsafe_allow_html=True)

st.success(
    f"✅ {len(CANDIDATOS) - 1} candidatos oficiales inscritos ante el JNE")

# ── Tabs ─────────────────────────────────────────────────────────
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
            verificar_limite()
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
                    verificar_limite()
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
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding: 1rem 0;">
    <p style="color:#6c757d; font-size:0.78rem; margin-bottom:0.8rem;">
        Información de fuentes públicas y búsqueda web en tiempo real.<br>
        Proyecto educativo y apartidario · Verifica en fuentes oficiales:
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
