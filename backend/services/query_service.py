from flask import Flask, request, jsonify
import openai 
from openai import OpenAI
import os
from dotenv import load_dotenv
from astroquery.simbad import Simbad
from astroquery.vizier import Vizier
import pyvo as vo

# Cargar las variables de entorno (OPENAI_API_KEY)
load_dotenv()

app = Flask(__name__)

# Configurar la clave de OpenAI desde .env
openai.api_key = os.getenv("OPENAI_API_KEY")
# Cliente para Deepseek
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

def classify_query(user_message, ai):
    """
    Clasifica una consulta en una de las categorías definidas para observatorios virtuales.
    
    Categorías posibles:
      - SIA: Imágenes
      - SSA: Espectros
      - SCS: Búsqueda de objetos
      - SLA: Líneas espectrales
      - REGISTRY: Descubrimiento de servicios

    Args:
        user_message (str): Consulta del usuario.
        ai (str): Identificador de la API a utilizar ("openai" o "deepseek").
    
    Returns:
        dict: Diccionario con la clasificación de la consulta.
    """
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert assistant in Astronomy and Virtual Observatories. "
                "Analyze the user's query and respond with a JSON object containing two keys: 'category' and 'object'. "
                "'category' should be one of the following: 'SIA' (images), 'SSA' (spectra), 'SCS' (object search), "
                "'SLA' (spectral lines), or 'REGISTRY' (service discovery). "
                "'object' should be a list of names or identifiers that can be used to search for the astronomical object in SIMBAD. "
                "Include all known designations such as Messier numbers (e.g., 'M42'), NGC/IC numbers (e.g., 'NGC 224'), common names (e.g., 'Andromeda Galaxy'), "
                "and other catalog identifiers (e.g., '2MASS J00361617+1821104', 'PSR B1919+21'). "
                "If no object is mentioned, return an empty list. "
                "If the user query is not a any specific object, return a random object from SIMBAD. "
                "Respond only with the JSON object, no explanations."
            ),
        },
        {"role": "user", "content": user_message},
    ]

    # Seleccionar la API en función del parámetro 'ai'
    if ai == "openai":
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    elif ai == "deepseek":
        response = client.ChatCompletion.create(
            model="gpt-4o",  # Asumiendo que el modelo es el mismo; si no, ajusta según corresponda.
            messages=messages,
            api_key=os.getenv("DEEPSEEK_API_KEY")
        )
    else:
        raise ValueError("El parámetro 'ai' debe ser 'openai' o 'deepseek'")

    response_text = response["choices"][0]["message"]["content"]
    # Eliminar delimitadores de código si están presentes
    response_text = response_text.replace("```json", "").replace("```", "")
    # Convertir la respuesta en un diccionario
    response_json = eval(response_text)
    return response_json


def coordinate_resolver_vizier(object_names):
    """
    Resuelve el nombre de un objeto astronómico en coordenadas (RA, Dec) usando VizieR.
    
    Args:
        object_names (list): Lista de posibles nombres del objeto astronómico.

    Returns:
        tuple or None: Tupla con las coordenadas (RA, Dec) del primer nombre válido encontrado, o None si ninguno es válido.
    """
    viz = Vizier(columns=["RAJ2000", "DEJ2000"])  # Definir columnas de coordenadas RA y Dec
        # Intentar realizar la consulta en VizieR
    result = viz.query_object(object_names[0])  # Realizar la consulta con el primer nombre

    # Verificar si la respuesta contiene datos
    if result:
        result_table = result[0]  # Accede a la primera tabla de resultados
        
        # Verifica si las columnas RA/Dec están presentes
        if "RAJ2000" in result_table.colnames and "DEJ2000" in result_table.colnames:
            ra = result_table["RAJ2000"][0]  # Coordenada RA
            dec = result_table["DEJ2000"][0]  # Coordenada Dec
            return ra, dec  # Retorna las coordenadas
    return None

def sia2 (user_message, object_name, coordinates):
    """
    Servicio de Imágenes Astronómicas (SIA).
    
    Args:
        user_message (str): Consulta del usuario.
    
    Returns:
        dict: JSON con la respuesta del bot.
    """
    client = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": ("You are a link generator for retrieving astronomical images using the Simple Image Access (SIA) protocol. "
                "When a client provides the name of an astronomical object or its coordinates, your task is to generate a URL that retrieves an image of that object from a specified resource. "
                "If the client provides the name of an object (such as Andromeda,Mars,etc.), you must convert it into sky coordinates (RA/Dec). "
                "If the client provides RA/Dec directly, use those coordinates. "
                "Then, use a VO service like NASA SkyView, SDSS, or CDS Aladin to generate the query link. "
                "Format the RA and Dec coordinates correctly for the SIA query and include the field size (if provided) in degrees. "
                "Finally, generate and return only the appropriate URL that points to the relevant service and provides an image in formats like PNG, JPEG, or FITS. "
                "Examples of URLs that work with the protocol are: SDSS (Sloan Digital Sky Survey): https://skyserver.sdss.org/dr14/SkyServerWS/ImgCutout/getjpeg?ra=10.6847083&dec=41.26875&scale=0.2&width=512&height=512&opt=G, "
                "CDS Aladin: http://cdsportal.u-strasbg.fr/?target=10.684%2C-41.2692 or http://cdsportal.u-strasbg.fr/?target=SgrA* , and SDSS (Another Example): https://skyserver.sdss.org/dr12/SkyserverWS/ImgCutout/getjpeg?ra=180.0&dec=45.0&scale=0.1&width=500&height=500. ALMA: https://almascience.nrao.edu/aq/?raDec=13:37:00.89%20-29:51:59.8"
                "Generate only URLs in the same structure using the appropriate coordinates and parameters for the client request."
                "Only generate the URL, no explanations."     
    ),          
            },
            {"role": "user", "content": user_message, "object": object_name, "coordinates": coordinates},
        ],
        api_key=openai.api_key,
    )
 

    response_url = client["choices"][0]["message"]["content"]
    # Devolver el diccionario con la respuesta
    return response_url

@app.route("/execute", methods=["POST"])
def execute():
    try:
        data = request.get_json()
        user_message = data.get("code")  # Recibimos el mensaje del usuario
        ai = data.get("ai")
        print("User message:", user_message)
        if not user_message:
            return jsonify({"error": "No se recibió un mensaje válido."}), 400

        # Clasificar la consulta del usuario
        classification = classify_query(user_message, ai)
        print("Classification:", classification)

        category = classification.get("category")
        object_name = classification.get("object")

        if category is None:
            return jsonify({"error": "No se pudo clasificar la consulta."}), 400
        
        elif category == "SIA":
            coordinates = coordinate_resolver_vizier(object_name)
            print("Coordinates:", coordinates)
            response = sia2(user_message, object_name, coordinates)
            print("Response:", response)
            return jsonify({"bot_response": response}), 200       
        
        elif category == "SSA":
            return jsonify({"bot_response": "SSA"}), 200
        
        elif category == "SCS":
            return jsonify({"bot_response": "SCS"}), 200
        
        elif category == "SLA":
            return jsonify({"bot_response": "SLA"}), 200
        
        elif category == "REGISTRY":
            return jsonify({"bot_response": "REGISTRY"}), 200
        else:
            return jsonify({"bot_response": "Otra categoría"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
