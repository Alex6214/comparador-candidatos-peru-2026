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
        credenciales = Credentials.from_service_account_file(
            ".streamlit/google_credentials.json",
            scopes=SCOPES
        )
    except Exception:
        # Lee desde secrets de Streamlit Cloud
        info = {
            "type": st.secrets["google_credentials"]["type"],
            "project_id": st.secrets["google_credentials"]["project_id"],
            "private_key_id": st.secrets["google_credentials"]["private_key_id"],
            "private_key": st.secrets["google_credentials"]["private_key"].replace("\\n", "\n"),
            "client_email": st.secrets["google_credentials"]["client_email"],
            "client_id": st.secrets["google_credentials"]["client_id"],
            "auth_uri": st.secrets["google_credentials"]["auth_uri"],
            "token_uri": st.secrets["google_credentials"]["token_uri"],
        }
        credenciales = Credentials.from_service_account_info(
            info,
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
        return True, None
    except Exception as e:
        return False, str(e)
