import streamlit as st
import pandas as pd
import requests

# Configura tu token de Hugging Face desde secrets.toml
API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/deepseek-llm-7b-chat"
headers = {"Authorization": f"Bearer {st.secrets['hf']['token']}"}

st.set_page_config(page_title="Chat con CSV (DeepSeek)", layout="centered")

st.title("📊 Chat con tu CSV usando DeepSeek")
st.write("Este asistente responde preguntas sobre un CSV ya cargado usando el modelo DeepSeek vía Hugging Face.")

# Cargar el CSV localmente
df = pd.read_csv("datos.csv")

# Mostrar una vista previa del CSV
st.subheader("Vista previa del CSV:")
st.dataframe(df)

# Campo de texto para pregunta
pregunta = st.text_input("Haz una pregunta sobre los datos:")

if pregunta:
    columnas = ", ".join(df.columns)
    resumen = df.describe(include='all').to_string()

    prompt = f"""Eres un experto en análisis de datos. Tienes este DataFrame:
Columnas: {columnas}
Resumen estadístico:\n{resumen}

Pregunta: {pregunta}
Responde de forma clara, basada únicamente en los datos."""

    payload = {
        "inputs": prompt,
        "parameters": {"temperature": 0.7, "max_new_tokens": 512},
    }

    with st.spinner("Generando respuesta con DeepSeek..."):
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            generated = response.json()[0]['generated_text'].replace(prompt, "").strip()
            st.markdown("### 🧠 Respuesta:")
            st.write(generated)
        else:
            st.error(f"Error {response.status_code}: {response.text}")
