import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configurar la clave API desde los secrets de Streamlit
genai.configure(api_key=st.secrets["gemini"]["api_key"])

st.set_page_config(page_title="Chat con CSV usando Gemini", layout="centered")

st.title("📊 Chat con tu CSV (Gemini)")
st.write("Este asistente responde preguntas sobre un CSV ya cargado usando Google Gemini.")

# Cargar el CSV fijo
df = pd.read_csv("datos.csv")

# Mostrar vista previa
st.subheader("Vista previa del CSV:")
st.dataframe(df)

# Pregunta del usuario
pregunta = st.text_input("Haz una pregunta sobre los datos:")

if pregunta:
    columnas = ", ".join(df.columns)
    resumen = df.describe(include='all').to_string()

    prompt = f"""
Actúa como un experto en análisis de datos. Este es un resumen de un DataFrame:
Columnas: {columnas}
Resumen estadístico:\n{resumen}

Pregunta: {pregunta}
Responde de forma clara, precisa y únicamente con base en los datos.
"""

    try:
        model = genai.GenerativeModel("gemini-pro")
        respuesta = model.generate_content(prompt)

        st.markdown("### 🧠 Respuesta:")
        st.write(respuesta.text)

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
