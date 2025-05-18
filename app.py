import streamlit as st
import pandas as pd
from openai import OpenAI

# Inicializa el cliente OpenAI usando clave desde secrets
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.set_page_config(page_title="Chat con CSV (ChatGPT)", layout="centered")
st.title("📊 Chat con tu CSV usando ChatGPT")
st.write("Este asistente responde preguntas sobre un CSV ya cargado usando ChatGPT (gpt-3.5-turbo).")

# Cargar el CSV
df = pd.read_csv("datos.csv")

# Mostrar vista previa
st.subheader("Vista previa del CSV:")
st.dataframe(df)

# Campo de texto para la pregunta
pregunta = st.text_input("Haz una pregunta sobre los datos:")

if pregunta:
    columnas = ", ".join(df.columns)
    resumen = df.describe(include='all').to_string()

    prompt = f"""Eres un experto en análisis de datos. Este es el resumen de un DataFrame:
Columnas: {columnas}
Resumen estadístico:\n{resumen}

Pregunta: {pregunta}
Responde de forma clara, detallada y solo usando los datos del CSV."""

    try:
        respuesta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en análisis de datos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        st.markdown("### 🧠 Respuesta:")
        st.write(respuesta.choices[0].message.content)

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
