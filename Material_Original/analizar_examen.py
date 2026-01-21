import json

def obtener_contrario(respuesta):
    mapa_contrarios = {
        "totalmente en desacuerdo": "totalmente de acuerdo",
        "en desacuerdo": "de acuerdo",
        "neutral": "neutral",
        "de acuerdo": "en desacuerdo",
        "totalmente de acuerdo": "totalmente en desacuerdo"
    }
    return mapa_contrarios.get(respuesta.lower(), respuesta)

def analizar_examen(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_archivo}")
        return

    preguntas = data.get("preguntas_y_respuestas", [])
    correcciones = []
    correctas_directas = []

    print(f"Analizando {len(preguntas)} preguntas del examen '{data.get('informacion_del_examen', {}).get('nombre', 'Desconocido')}'...\n")

    for i, item in enumerate(preguntas, 1):
        pregunta = item.get("pregunta")
        seleccionada = item.get("seleccionada")
        puntaje = item.get("puntaje")
        
        es_correcta = puntaje == "1/1"
        
        respuesta_final = seleccionada if es_correcta else obtener_contrario(seleccionada)
        
        resultado = {
            "numero": i,
            "pregunta": pregunta,
            "respuesta_correcta": respuesta_final,
            "era_incorrecta": not es_correcta,
            "respuesta_original": seleccionada
        }
        
        if not es_correcta:
            correcciones.append(resultado)
        else:
            correctas_directas.append(resultado)

    # Imprimir reporte
    print("-" * 50)
    print("ERRORES DETECTADOS Y CORREGIDOS (Puntaje 0/1)")
    print("-" * 50)
    if correcciones:
        for c in correcciones:
            print(f"Pregunta: {c['pregunta']}")
            print(f"  ❌ Seleccionó: {c['respuesta_original']}")
            print(f"  ✅ Correcta sugerida (contrario): {c['respuesta_correcta']}")
            print("-" * 20)
    else:
        print("No se encontraron respuestas incorrectas con puntaje 0/1.")

    print("\n" + "=" * 50)
    print("GUIA COMPLETA DE RESPUESTAS CORRECTAS")
    print("=" * 50)
    
    todas_respuestas = sorted(correcciones + correctas_directas, key=lambda x: x['numero'])
    
    for item in todas_respuestas:
        estado = "🔄 CORREGIDA" if item['era_incorrecta'] else "✅ ORIGINAL"
        print(f"{item['numero']}. {item['pregunta']}")
        print(f"   Respuesta: {item['respuesta_correcta']} ({estado})")
        print()

    # Guardar versión corregida
    archivo_salida = ruta_archivo.replace('.json', '_corregido.json')
    data['preguntas_y_respuestas'] = [
        {
            "pregunta": item['pregunta'],
            "respuesta_correcta": item['respuesta_correcta']
        }
        for item in todas_respuestas
    ]
    
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Archivo corregido guardado en: {archivo_salida}")

if __name__ == "__main__":
    analizar_examen("c:/Users/X1 Carbon/Desktop/examenes militar pdfs/examen_axiologico.json")
