import streamlit as st
import pandas as pd
import os
from database import session, Usuario
from werkzeug.security import check_password_hash
from sqlalchemy.orm.exc import NoResultFound

# Configuración de la página
st.set_page_config(page_title="Autoclaves Dashboard", layout="wide")

# ---- Función para la autenticación ----
def autenticar_usuario(username, password):
    try:
        usuario = session.query(Usuario).filter_by(username=username).one()
        if check_password_hash(usuario.password, password):
            return True
        else:
            return False
    except NoResultFound:
        return False

# ---- Página de Login ----
if "usuario" not in st.session_state:
    st.session_state.usuario = None

if st.session_state.usuario is None:
    st.title("🔒 Iniciar Sesión")

    username = st.text_input("Usuario", key="username")
    password = st.text_input("Contraseña", type="password", key="password")
    login_btn = st.button("Iniciar sesión")

    if login_btn:
        if autenticar_usuario(username, password):
            st.session_state.usuario = username
            st.success("✅ Inicio de sesión exitoso")
            st.rerun()  # <--- Corrección: antes era st.experimental_rerun()
        else:
            st.error("⚠️ Usuario o contraseña incorrectos.")
    
    st.stop()

# ---- Interfaz después del login ----
st.sidebar.title(f"👤 Usuario: {st.session_state.usuario}")
st.sidebar.button("Cerrar sesión", on_click=lambda: st.session_state.update({"usuario": None, "archivos": []}), key="logout")
st.title("📊 Dashboard de Autoclaves")

# ---- Subir archivos CSV ----
st.sidebar.subheader("📂 Cargar archivos CSV")
archivos_subidos = st.sidebar.file_uploader("Selecciona uno o varios archivos CSV", accept_multiple_files=True, type=["csv"])

if "archivos" not in st.session_state:
    st.session_state.archivos = []

if archivos_subidos:
    for archivo in archivos_subidos:
        st.session_state.archivos.append(archivo)

# ---- Mostrar los datos cargados ----
if st.session_state.archivos:
    for archivo in st.session_state.archivos:
        try:
            df = pd.read_csv(archivo, delimiter=';', skipinitialspace=True)
            df.columns = ["Fecha", "Hora", "Autoclave"]
            df["Tiempo"] = pd.to_datetime(df["Fecha"] + " " + df["Hora"], dayfirst=True)
            df = df.sort_values("Tiempo")

            st.subheader(f"📌 Datos del archivo: {archivo.name}")
            st.line_chart(df.set_index("Tiempo")["Autoclave"])

        except Exception as e:
            st.error(f"⚠️ Error al procesar {archivo.name}: {e}")

else:
    st.info("📎 No se han subido archivos aún.")

