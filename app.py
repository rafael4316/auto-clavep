import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import session, RegistroAutoclave, Usuario
import datetime

# Configuración de la página
st.set_page_config(page_title="Autoclaves Dashboard", layout="wide")

# ---- Autenticación de Usuarios ----
def autenticar_usuario(username, password):
    usuario = session.query(Usuario).filter_by(username=username, password=password).first()
    return usuario is not None

if "usuario" not in st.session_state:
    with st.form("login_form"):
        st.subheader("🔐 Iniciar Sesión")
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Iniciar Sesión")

        if submit:
            if autenticar_usuario(username, password):
                st.session_state.usuario = username
                st.experimental_rerun()
            else:
                st.error("⚠️ Usuario o contraseña incorrectos.")

if "usuario" in st.session_state:
    st.sidebar.success(f"Bienvenido, {st.session_state.usuario}")

    # ---- Menú lateral ----
    menu = st.sidebar.radio("Menú", ["📂 Subir Datos", "📊 Historial de Registros"])

    # ---- Subir archivos CSV ----
    if menu == "📂 Subir Datos":
        st.title("📂 Cargar Archivo CSV")
        archivos_subidos = st.file_uploader("Selecciona archivos CSV", accept_multiple_files=True, type=["csv"])

        if archivos_subidos:
            for archivo in archivos_subidos:
                df = pd.read_csv(archivo, delimiter=';', skipinitialspace=True)
                df.columns = ["Fecha", "Hora", "Autoclave"]
                df["Tiempo"] = pd.to_datetime(df["Fecha"] + " " + df["Hora"], dayfirst=True)
                df = df.sort_values("Tiempo")

                # Guardar en base de datos
                nuevo_registro = RegistroAutoclave(nombre_archivo=archivo.name, autoclave=df["Autoclave"].iloc[0])
                session.add(nuevo_registro)
                session.commit()

                # Graficar
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(df["Tiempo"], df["Autoclave"], linestyle='-', linewidth=1.5, color='black')
                ax.set_xlabel("Tiempo")
                ax.set_ylabel("Temperatura / Presión")
                ax.set_title(f"Autoclave {df['Autoclave'].iloc[0]}")
                ax.grid(True, linestyle="--", linewidth=0.5)
                st.pyplot(fig)

    # ---- Historial de Registros ----
    elif menu == "📊 Historial de Registros":
        st.title("📊 Historial de Datos Cargados")
        
        registros = session.query(RegistroAutoclave).all()
        
        if registros:
            for registro in registros:
                st.subheader(f"📌 {registro.nombre_archivo} - Autoclave {registro.autoclave}")
                st.write(f"📅 Fecha: {registro.fecha_subida}")
        else:
            st.info("⚠️ No hay registros almacenados aún.")

    # ---- Cerrar sesión ----
    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state.usuario
        st.experimental_rerun()
