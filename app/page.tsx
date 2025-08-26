'use client'

import { useState, useCallback } from 'react'
import Papa from 'papaparse'
import { MessageSquare, Loader2 } from 'lucide-react'

interface CSVData {
  headers: string[]
  rows: any[][]
  sample: string
  columnSummary: string
}

export default function Home() {
  const [csvData, setCsvData] = useState<CSVData | null>(null)
  const [pregunta, setPregunta] = useState('')
  const [respuesta, setRespuesta] = useState('')
  const [loading, setLoading] = useState(false)

  const procesarCSV = useCallback((data: any[], headers: string[]) => {
    // Crear muestra aleatoria (máximo 30 filas)
    const sampleSize = Math.min(data.length, 30)
    const shuffled = [...data].sort(() => 0.5 - Math.random())
    const sampleData = shuffled.slice(0, sampleSize)
    
    // Convertir muestra a string
    const sampleString = [headers.join('\t'), ...sampleData.map(row => 
      headers.map(header => row[header] || '').join('\t')
    )].join('\n')
    
    // Crear resumen de columnas
    const columnSummary = headers.map(header => {
      const values = data.map(row => row[header]).filter(v => v !== undefined && v !== '')
      const uniqueValues = [...new Set(values)].slice(0, 5)
      const dataType = typeof values[0] === 'number' ? 'number' : 'string'
      return `${header} (${dataType}): ${JSON.stringify(uniqueValues)}`
    }).join('\n')
    
    return {
      headers,
      rows: data,
      sample: sampleString,
      columnSummary
    }
  }, [])

  const cargarCSVPorDefecto = useCallback(async () => {
    try {
      const response = await fetch(`${window.location.origin}/datos.csv`)
      const csvText = await response.text()
      
      Papa.parse(csvText, {
        header: true,
        skipEmptyLines: true,
        complete: (results) => {
          const processedData = procesarCSV(results.data, results.meta.fields || [])
          setCsvData(processedData)
        }
      })
    } catch (error) {
      console.error('Error cargando CSV por defecto:', error)
    }
  }, [procesarCSV])



  const enviarPregunta = async () => {
    if (!pregunta.trim() || !csvData) return
    
    setLoading(true)
    setRespuesta('')
    
    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          pregunta,
          resumenColumnas: csvData.columnSummary,
          muestra: csvData.sample
        })
      })
      
      const data = await response.json()
      
      if (data.error) {
        setRespuesta(`Error: ${data.error}`)
      } else {
        setRespuesta(data.respuesta)
      }
    } catch (error) {
      setRespuesta('Error al procesar la consulta. Inténtalo de nuevo.')
    } finally {
      setLoading(false)
    }
  }

  // Cargar CSV por defecto al montar el componente
  useState(() => {
    cargarCSVPorDefecto()
  })

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">📊 Explorador de datos</h1>
          <p className="text-gray-600">Haz preguntas en lenguaje natural sobre tu CSV. La app sintetiza la respuesta basándose en el contenido del fichero.</p>
        </div>

        <div className="space-y-6">
            {/* Vista previa del CSV */}
            {csvData && (
              <div className="custom-card">
                <h3 className="text-lg font-semibold mb-4">📄 Vista previa (primeras filas)</h3>
                <div className="overflow-x-auto">
                  <table className="min-w-full text-sm">
                    <thead>
                      <tr className="bg-gray-50">
                        {csvData.headers.map((header, index) => (
                          <th key={index} className="px-3 py-2 text-left font-medium text-gray-700 border-b">
                            {header}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {csvData.rows.slice(0, 10).map((row, rowIndex) => (
                        <tr key={rowIndex} className="hover:bg-gray-50">
                          {csvData.headers.map((header, colIndex) => (
                            <td key={colIndex} className="px-3 py-2 border-b text-gray-600">
                              {row[header]}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Consulta */}
            <div className="custom-card">
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <MessageSquare className="w-5 h-5" />
                Consulta tus datos
              </h3>
              
              <div className="space-y-4">
                <input
                  type="text"
                  value={pregunta}
                  onChange={(e) => setPregunta(e.target.value)}
                  placeholder="Ej.: ¿Cuál es la media de ventas por región en 2024?"
                  className="w-full custom-input"
                  onKeyPress={(e) => e.key === 'Enter' && enviarPregunta()}
                />
                
                <button
                  onClick={enviarPregunta}
                  disabled={!pregunta.trim() || !csvData || loading}
                  className="custom-button disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Analizando...
                    </>
                  ) : (
                    'Enviar consulta'
                  )}
                </button>
              </div>
            </div>

            {/* Resultado */}
            {respuesta && (
              <div className="custom-card">
                <h3 className="text-lg font-semibold mb-4">Resultado</h3>
                <div className="prose prose-sm max-w-none">
                  <p className="whitespace-pre-wrap text-gray-700">{respuesta}</p>
                </div>
              </div>
            )}
        </div>
      </div>
    </div>
  )
}