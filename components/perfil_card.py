import streamlit as st


def mostrar_perfil(candidato: dict, perfil: dict):
    nombre = candidato["nombre"]
    partido = candidato["partido"]

    ideologia = perfil.get("posicion_ideologica", "No disponible")
    color_ideo = {
        "izquierda": "#dc3545",
        "centro-izquierda": "#fd7e14",
        "centro": "#6c757d",
        "centro-derecha": "#0d6efd",
        "derecha": "#0a58ca"
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
