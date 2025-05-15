import streamlit as st
import pandas as pd
import openai

openai.api_key = st.secrets["openai"]["api_key"]

st.title("Chat con tu CSV fijo")
st.write("Este asistente responde preguntas sobre un CSV ya cargado.")

# Cargar CSV directamente del repo
df = pd.read_csv("datos.csv")
st.write("Vista previa del CSV:", df.head())

# Campo de pregunta
pregunta = st.text_input("Haz una pregunta sobre los datos:")

if pregunta:
    resumen = df.describe(include='all').to_string()
    columnas = ", ".join(df.columns)

    prompt = f"""
Actúa como un asistente de datos. Responde preguntas sobre el siguiente DataFrame:
Columnas: {columnas}
Resumen estadístico:\n{resumen}
Pregunta del usuario: {pregunta}
Responde de forma clara y concisa.
"""

    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente experto en análisis de datos."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    st.markdown("**Respuesta:**")
    st.write(respuesta["choices"][0]["message"]["content"])
