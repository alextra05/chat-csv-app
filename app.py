import streamlit as st
import pandas as pd
import requests

# Configura tu token de DeepSeek desde secrets.toml
API_URL = "https://api.deepseek.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {st.secrets['deepseek']['token']}",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="Chat con CSV (DeepSeek)", layout="centered")
st.title("📊 Chat con tu CSV usando DeepSeek")
st.write("Este asistente responde preguntas sobre un CSV ya cargado usando el modelo DeepSeek vía su API oficial.")

# Cargar el CSV localmente
df = pd.read_csv("datos.csv")

# Mostrar vista previa del DataFrame
st.subheader("Vista previa del CSV:")
st.dataframe(df)

# Pregunta del usuario
pregunta = st.text_input("Haz una pregunta sobre los datos:")

if pregunta:
    columnas = ", ".join(df.columns)
    resumen = df.describe(include='all').to_string()

    prompt = f"""Eres un experto en análisis de datos. Este es el resumen de un DataFrame:
Columnas: {columnas}
Resumen estadístico:\n{resumen}

Pregunta: {pregunta}
Responde de forma clara y precisa, usando solo los datos."""

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Eres un asistente útil."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }

    with st.spinner("Generando respuesta con DeepSeek..."):
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            generated = response.json()["choices"][0]["message"]["content"].strip()
            st.markdown("### 🧠 Respuesta:")
            st.write(generated)
        else:
            st.error(f"Error {response.status_code}: {response.text}")
