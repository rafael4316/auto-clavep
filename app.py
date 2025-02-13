import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="Visualizador de Autoclave", layout="wide")

# Estilos personalizados
st.markdown("""
    <style>
    .css-18e3th9 {
        padding-top: 2rem;
    }
    .css-1d391kg {
        padding-top: 1rem;
    }
    .stApp {
        background-color: #f7f9fc;
    }
    </style>
    """, unsafe_allow_html=True)

# Título principal
st.title("📊 Visualizador de Datos de Autoclave")

# Sección de carga de archivos
st.sidebar.header("📂 Cargar Archivos CSV")
archivos = st.sidebar.file_uploader("Selecciona uno o varios archivos CSV", type=["csv"], accept_multiple_files=True)

# Validar que se haya cargado al menos un archivo
if archivos:
    st.sidebar.subheader("📋 Archivos cargados")
    nombres_archivos = [archivo.name for archivo in archivos]
    archivo_seleccionado = st.sidebar.selectbox("Selecciona un archivo para visualizar", nombres_archivos)

    # Obtener el archivo seleccionado
    archivo_actual = next(archivo for archivo in archivos if archivo.name == archivo_seleccionado)

    try:
        # Leer el archivo seleccionado
        df = pd.read_csv(archivo_actual, delimiter=';', skipinitialspace=True)
        df.columns = ["Fecha", "Hora", "Autoclave_02"]
        df["Tiempo"] = pd.to_datetime(df["Fecha"] + " " + df["Hora"], dayfirst=True)
        df = df.sort_values("Tiempo")

        # Mostrar dataframe
        with st.expander("📋 Vista previa de los datos", expanded=False):
            st.dataframe(df)

        # Graficar datos
        st.subheader("📈 Gráfico de Autoclave")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df["Tiempo"], df["Autoclave_02"], linestyle='-', linewidth=1.5, color='black')
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Temperatura / Presión")
        ax.set_title(f"Autoclave Nº1 - {archivo_seleccionado}")
        ax.grid(True, linestyle="--", linewidth=0.5)
        st.pyplot(fig)

        # Guardar gráfico en PDF
        buffer = BytesIO()
        fig.savefig(buffer, format="pdf")
        buffer.seek(0)
        st.sidebar.download_button(label="📄 Descargar Gráfico en PDF", data=buffer, file_name=f"grafico_{archivo_seleccionado}.pdf", mime="application/pdf")

    except Exception as e:
        st.error(f"⚠️ Error al procesar el archivo: {e}")

else:
    st.warning("🔹 Carga uno o más archivos CSV desde la barra lateral para comenzar.")
