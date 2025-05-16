import streamlit as st
import pandas as pd
import requests

# URL del modelo en Hugging Face
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {"Authorization": f"Bearer {st.secrets['hf']['token']}"}

st.set_page_config(page_title="Chat con CSV (Mistral)", layout="centered")

st.title("📊 Chat con tu CSV usando Mistral")
st.write("Este asistente responde preguntas sobre un CSV ya cargado usando el modelo Mistral 7B Instruct desde Hugging Face.")

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
Responde de forma clara, detallada y solo usando los datos del CSV."""

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 512
        }
    }

    with st.spinner("Generando respuesta con Mistral..."):
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            generated = response.json()[0]['generated_text'].replace(prompt, "").strip()
            st.markdown("### 🧠 Respuesta:")
            st.write(generated)
        else:
            st.error(f"Error {response.status_code}: {response.text}")
