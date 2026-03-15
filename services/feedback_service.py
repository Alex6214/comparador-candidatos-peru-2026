import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


def get_sheet():
    try:
        # Intenta leer desde archivo local
        credenciales = Credentials.from_service_account_file(
            ".streamlit/google_credentials.json",
            scopes=SCOPES
        )
        print("✅ Credenciales cargadas desde archivo local")
    except Exception as e1:
        print(f"⚠️ Archivo local no encontrado: {e1}")
        try:
            # Lee desde Streamlit Cloud secrets
            info = {
                "type": str(st.secrets["google_credentials"]["type"]),
                "project_id": str(st.secrets["google_credentials"]["project_id"]),
                "private_key_id": str(st.secrets["google_credentials"]["private_key_id"]),
                "private_key": str(st.secrets["google_credentials"]["private_key"]).replace("\\n", "\n"),
                "client_email": str(st.secrets["google_credentials"]["client_email"]),
                "client_id": str(st.secrets["google_credentials"]["client_id"]),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
            print(f"📧 Usando client_email: {info['client_email']}")
            credenciales = Credentials.from_service_account_info(
                info, scopes=SCOPES
            )
            print("✅ Credenciales cargadas desde secrets")
        except Exception as e2:
            print(f"❌ Error cargando credenciales desde secrets: {e2}")
            raise e2

    try:
        cliente = gspread.authorize(credenciales)
        sheet = cliente.open(st.secrets["GOOGLE_SHEET_NAME"])
        print(f"✅ Sheet abierto: {st.secrets['GOOGLE_SHEET_NAME']}")
        return sheet.sheet1
    except Exception as e3:
        print(f"❌ Error abriendo sheet: {e3}")
        raise e3


def guardar_feedback(nombre: str, comentario: str, voto: str):
    try:
        sheet = get_sheet()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([fecha, nombre, comentario, voto])
        print(f"✅ Feedback guardado: {nombre} - {voto}")
        return True, None
    except Exception as e:
        print(f"❌ Error guardando feedback: {e}")
        return False, str(e)
