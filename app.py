import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy.orm import sessionmaker
from database import engine, Usuario, ArchivoSubido  # Importar modelos de la BD
import datetime
from werkzeug.security import check_password_hash  # Importar para comparar contraseñas

# Crear sesión con la base de datos
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Configurar sesión de usuario
if "usuario_autenticado" not in st.session_state:
    st.session_state.usuario_autenticado = None
    
# Función para verificar credenciales
def autenticar(usuario, password):
    usuario_db = session.query(Usuario).filter_by(username=usuario).first()
    if usuario_db and check_password_hash(usuario_db.password, password):
        return True
    return False
    
# Interfaz de login
if st.session_state.usuario_autenticado is None:
    st.title("🔒 Iniciar Sesión")
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if autenticar(usuario, password):
            st.session_state.usuario_autenticado = usuario
            st.success(f"Bienvenido, {usuario} 🎉")
            st.experimental_rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos")

# Si el usuario está autenticado, mostrar la app
if st.session_state.usuario_autenticado:
    st.title("📊 Visualizador de Autoclaves")

    # Subir múltiples archivos CSV
    archivos = st.file_uploader("📂 Cargar archivos CSV", accept_multiple_files=True, type=["csv"])

    if archivos:
        fig, ax = plt.subplots(figsize=(10, 5))
        
        for archivo in archivos:
            df = pd.read_csv(archivo, delimiter=';', skipinitialspace=True)
            df.columns = ["Fecha", "Hora", "Autoclave_02"]
            df["Tiempo"] = pd.to_datetime(df["Fecha"] + " " + df["Hora"], dayfirst=True)
            df = df.sort_values("Tiempo")

            ax.plot(df["Tiempo"], df["Autoclave_02"], linestyle='-', linewidth=1.5, label=archivo.name)

            # Guardar en la base de datos
            nuevo_archivo = ArchivoSubido(
                usuario=st.session_state.usuario_autenticado,
                archivo_nombre=archivo.name,
                fecha_subida=datetime.datetime.utcnow()
            )
            session.add(nuevo_archivo)
            session.commit()

        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Temperatura / Presión")
        ax.set_title("Datos de Autoclaves")
        ax.legend()
        ax.grid(True, linestyle="--", linewidth=0.5)
        
        st.pyplot(fig)

    # Mostrar el historial de archivos cargados
    st.subheader("📌 Archivos Subidos")
    archivos_subidos = session.query(ArchivoSubido).filter_by(usuario=st.session_state.usuario_autenticado).all()

    if archivos_subidos:
        for archivo in archivos_subidos:
            st.write(f"📄 {archivo.archivo_nombre} - {archivo.fecha_subida.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        st.write("No hay archivos subidos.")

    # Botón de cerrar sesión
    if st.button("🔓 Cerrar sesión"):
        st.session_state.usuario_autenticado = None
        st.experimental_rerun()
