import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st
import json

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


@st.cache_resource
def get_sheet():
    try:
        # Intenta leer desde el archivo JSON local (desarrollo en tu Mac)
        credenciales = Credentials.from_service_account_file(
            ".streamlit/google_credentials.json",
            scopes=SCOPES
        )
    except Exception:
        # Si no encuentra el archivo lee desde Streamlit Cloud secrets
        credenciales = Credentials.from_service_account_info(
            dict(st.secrets["google_credentials"]),
            scopes=SCOPES
        )

    cliente = gspread.authorize(credenciales)
    sheet = cliente.open(st.secrets["GOOGLE_SHEET_NAME"])
    return sheet.sheet1


def guardar_feedback(nombre: str, comentario: str, voto: str):
    try:
        sheet = get_sheet()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([fecha, nombre, comentario, voto])
        return True
    except Exception as e:
        # Mostramos el error exacto en pantalla para saber qué falla
        st.error(f"Error detallado: {e}")
        return False
