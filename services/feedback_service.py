import requests
from datetime import datetime
import streamlit as st


def guardar_feedback(nombre: str, comentario: str, voto: str):
    try:
        # Datos a enviar al Google Sheet
        datos = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nombre": nombre,
            "comentario": comentario,
            "voto": voto
        }

        # Enviamos los datos a Google Apps Script via POST
        respuesta = requests.post(
            st.secrets["GOOGLE_SCRIPT_URL"],
            json=datos,
            timeout=10
        )

        # Verificamos que la respuesta sea exitosa
        resultado = respuesta.json()
        if resultado.get("resultado") == "ok":
            return True, None
        else:
            return False, resultado.get("mensaje", "Error desconocido")

    except Exception as e:
        return False, str(e)
