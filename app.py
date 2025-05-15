import streamlit as st
import pandas as pd
from openai import OpenAI

# Inicializar cliente OpenAI
client = OpenAI()
openai_api_key = st.secrets["openai"]["api_key"]

st.set_page_config(page_title="Chat con tu CSV fijo", layout="centered")

st.title("📊 Chat con tu CSV fijo")
st.write("Este asistente responde preguntas sobre un CSV ya cargado.")

# Cargar CSV
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
Actúa como un analista de datos. Responde preguntas sobre este DataFrame de empleados.
Columnas disponibles: {columnas}
Resumen estadístico:\n{resumen}
Pregunta: {pregunta}
Responde de forma clara y precisa, usando solo los datos.
"""

    try:
        respuesta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en análisis de datos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        st.markdown("### 🧠 Respuesta:")
        st.write(respuesta.choices[0].message.content)

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
