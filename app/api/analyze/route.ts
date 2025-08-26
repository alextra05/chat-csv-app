import { NextRequest, NextResponse } from 'next/server'
import OpenAI from 'openai'

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
})

export async function POST(request: NextRequest) {
  try {
    const { pregunta, resumenColumnas, muestra } = await request.json()

    if (!pregunta || !resumenColumnas || !muestra) {
      return NextResponse.json(
        { error: 'Faltan parámetros requeridos' },
        { status: 400 }
      )
    }

    const prompt = `
Eres un analista de datos. Responde de forma precisa y verificable SOLO en base al CSV proporcionado.
Si la pregunta no puede responderse con los datos, dilo con claridad y sugiere qué columna(s) faltan.

Resumen por columna:
${resumenColumnas}

Muestra del DataFrame (30 filas o menos):
${muestra}

Pregunta del usuario:
${pregunta}

Instrucciones de salida:
- Da una respuesta breve y clara primero (2-4 frases).
- Si procede, muestra cálculos o agregados en formato texto.
- No inventes columnas ni valores.
`

    const completion = await client.chat.completions.create({
      model: 'gpt-4-turbo',
      messages: [
        {
          role: 'system',
          content: 'Eres un asistente experto en análisis de datos en español.',
        },
        {
          role: 'user',
          content: prompt,
        },
      ],
      temperature: 0.2,
    })

    const respuesta = completion.choices[0].message.content

    return NextResponse.json({ respuesta })
  } catch (error) {
    console.error('Error en la API:', error)
    return NextResponse.json(
      { error: 'Error interno del servidor' },
      { status: 500 }
    )
  }
}