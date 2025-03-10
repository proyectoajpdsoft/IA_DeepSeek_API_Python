import requests
import argparse

API_KEY_DEEPSEEK = "sk-e......5....1......d"
URL_API = "https://api.deepseek.com/v1/chat/completions"

# Mostrar y preparar los argumentos que admite el programa por la línea de comandos
def MostrarArgumentos():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pregunta", type=str, required=True,
        help="Pregunta que se hará a la IA")
    parser.add_argument("-m", "--modelo", type=str, required=False,
        help="Admite modelo deepseek-chat (establecido por defecto) o deepseek-reason")
    parser.add_argument("-e", "--evitar_explicaciones", type=bool, required=False,
        help="Evita mostrar explicaciones adicionales, activado por defecto")
    
    return parser.parse_args() 

# Realizar pregunta a la IA y obtener la respuesta
def realizarPreguntaIA (pregunta, modelo="deepseek-chat", explicaciones=True):
    try:
        # Definimos los encabezados HTTP para la petición, pasándole la API Key
        headers = {
            "Authorization": f"Bearer {API_KEY_DEEPSEEK}",
            "Content-Type": "application/json"
        }
        
        if explicaciones:
            pregunta = f"{pregunta}. NO muestres explicaciones, cíñete únicamente a mostrar lo que se te ha pedido"

        # Podremos usar el modelo deepseek-chat o bien deepseek-reasoner
        peticionIA = {
            "model": modelo,
            "messages": [{"role": "user", "content": pregunta}],
            "stream": False # para que devuelva la respuesta completa y directamente
        }

        respuestaIA = requests.post(URL_API, headers=headers, json=peticionIA)
        # Verificar si la solicitud fue exitosa
        if respuestaIA.status_code == 200:
            # Convertir la respuesta a JSON
            respuestaIAJSON = respuestaIA.json()            
            
            # Acceder al primera y única respuesta
            if "choices" in respuestaIAJSON and len(respuestaIAJSON["choices"]) > 0:
                    primeraRespuesta = respuestaIAJSON["choices"][0]
                    if "message" in primeraRespuesta:
                        # Acceder al campo "content" del JSON que contiene la respuesta            
                        contenido = primeraRespuesta["message"].get("content")
                        if contenido == None:
                            return "[ERROR] La IA no ha devuelto una respuesta. La primera respuesta no contiene el campo 'content'."
                        else:
                            # Devolver solo el contenido
                            return contenido
                    else:
                        return "[ERROR] La IA no ha devuelto una respuesta. La primera respuesta no contiene el campo 'message'."
            else:
                return "[ERROR] La IA no ha devuelto una respuesta."
        else:
            return f"[ERROR] Se ha producido un error al intentar usar la IA: {respuestaIA.status_code} {respuestaIA.text}."
    except Exception as e:
        return f"[ERROR] Se ha producido un error al intentar usar la IA: {e}."

# Probamos el método, queremos que únicamente devuelva la respuesta
# para poder usar esta app en otra app
if __name__ == "__main__":
    # Preparamos y mostramos los argumentos (si se indica)
    args = MostrarArgumentos()
    pregunta = ""
    modelo = "deepseek-chat"
    evitarExplicaciones = True
    if args.pregunta:
        pregunta = args.pregunta
    if args.modelo:
        modelo = args.modelo
    if args.evitar_explicaciones:
        evitarExplicaciones = args.evitar_explicaciones

    respuestaIA = realizarPreguntaIA(pregunta=pregunta, modelo=modelo, explicaciones=evitarExplicaciones)
    print(respuestaIA)