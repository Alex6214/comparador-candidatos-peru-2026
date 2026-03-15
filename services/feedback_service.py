import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


@st.cache_resource
def get_sheet():
    credenciales = Credentials.from_service_account_file(
        ".streamlit/google_credentials.json",
        scopes=SCOPES
    )
    cliente = gspread.authorize(credenciales)
    sheet = cliente.open(st.secrets["GOOGLE_SHEET_NAME"])
    return sheet.sheet1


def guardar_feedback(nombre: str, comentario: str, voto: str):
    try:
        sheet = get_sheet()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Orden: fecha, nombre, comentario, voto
        sheet.append_row([fecha, nombre, comentario, voto])
        return True
    except Exception as e:
        print(f"Error al guardar feedback: {e}")
        return False
