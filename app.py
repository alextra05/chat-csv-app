import streamlit as st
import pandas as pd
from openai import OpenAI

# Cliente OpenAI con clave desde secrets
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.set_page_config(page_title="Chat con CSV (GPT-4 Turbo)", layout="centered")
st.title("📊 Chat con tu CSV usando GPT-4 Turbo")
st.write("Este asistente responde preguntas sobre un CSV usando el modelo GPT-4 Turbo de OpenAI.")

# Cargar el CSV
df = pd.read_csv("datos.csv")

# Mostrar vista previa
st.subheader("Vista previa del CSV:")
st.dataframe(df)

# Preparar muestra y resumen por columnas
muestra = df.sample(min(len(df), 30), random_state=42).to_string(index=False)
resumen_columnas = "\n".join([
    f"{col} ({df[col].dtype}): {df[col].unique()[:5].tolist()}"
    for col in df.columns
])

# Pregunta del usuario
pregunta = st.text_input("Haz una pregunta sobre los datos:")

if pregunta:
    prompt = f"""
Eres un experto en análisis de datos. A continuación tienes:

Resumen por columna:
{resumen_columnas}

Muestra del DataFrame:
{muestra}

Pregunta: {pregunta}
Responde de forma precisa, clara y solo con base en los datos. Usa lenguaje técnico si es necesario.
"""

    try:
        respuesta = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en análisis de datos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        st.markdown("### 🧠 Respuesta:")
        st.write(respuesta.choices[0].message.content)

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
