import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import session, RegistroAutoclave, Usuario
import datetime

# Configuración de la página
st.set_page_config(page_title="Autoclaves Dashboard", layout="wide")

# Función para autenticación
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
    menu = st.sidebar.radio("Menú", ["📂 Subir Datos", "📊 Historial de Registros"])

    if menu == "📂 Subir Datos":
        st.title("📂 Cargar Archivo CSV")
        archivo = st.file_uploader("Selecciona un archivo CSV", type=["csv"])

        if archivo:
            df = pd.read_csv(archivo, delimiter=';', skipinitialspace=True)
            df.columns = ["Fecha", "Hora", "Autoclave"]
            df["Tiempo"] = pd.to_datetime(df["Fecha"] + " " + df["Hora"], dayfirst=True)
            df = df.sort_values("Tiempo")

            # Guardar en la base de datos
            nuevo_registro = RegistroAutoclave(nombre_archivo=archivo.name, autoclave=df["Autoclave"].iloc[0])
            session.add(nuevo_registro)
            session.commit()

            # ---- 📌 Gráfica Mejorada ----
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Graficar la temperatura/presión
            ax.plot(df["Tiempo"], df["Autoclave"], linestyle='-', linewidth=2, color='black')

            # Etiquetas y diseño mejorado
            ax.set_xlabel("Tiempo", fontsize=12, fontweight="bold")
            ax.set_ylabel("Temperatura (°C)", fontsize=12, fontweight="bold")
            ax.set_title(f"Autoclave N°{df['Autoclave'].iloc[0]}", fontsize=14, fontweight="bold")

            # Agregar cuadrícula y bordes
            ax.grid(True, linestyle="--", linewidth=0.5)

            # Límites y ticks
            ax.set_yticks(range(20, 150, 12))  # Ajustar intervalos del eje Y
            ax.set_xticks(df["Tiempo"][::30])  # Ajustar intervalos del eje X

            # 📌 Agregar información dentro de la gráfica
            detalle_x = df["Tiempo"].iloc[len(df)//2]
            detalle_y = df["Autoclave"].max() - 10
            ax.text(detalle_x, detalle_y, f"AG SA1\nFP: {df['Fecha'].iloc[0]}\nBatch: {df['Autoclave'].iloc[0]}", 
                    fontsize=10, ha="center", bbox=dict(facecolor="white", alpha=0.8))

            # 📌 Agregar nombre de la empresa arriba
            plt.figtext(0.5, 0.98, "PACIFIC NATURAL FOODS S.A.C", fontsize=14, fontweight="bold", ha="center")

            # Mostrar gráfico en Streamlit
            st.pyplot(fig)

    elif menu == "📊 Historial de Registros":
        st.title("📊 Historial de Datos Cargados")
        registros = session.query(RegistroAutoclave).all()
        if registros:
            for registro in registros:
                st.subheader(f"📌 {registro.nombre_archivo} - Autoclave {registro.autoclave}")
                st.write(f"📅 Fecha: {registro.fecha_subida}")
        else:
            st.info("⚠️ No hay registros almacenados aún.")

    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state.usuario
        st.experimental_rerun()
