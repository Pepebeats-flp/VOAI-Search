from flask import Flask, request, jsonify
from dotenv import load_dotenv
import pyvo
from astroquery.vizier import Vizier
import gpt_client
import deepseek_client
import requests
from PIL import Image
from io import BytesIO
import random
from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord
import astropy.units as u


# Cargar variables de entorno
load_dotenv()

# Importar módulos especializados
import gpt_client
import deepseek_client


app = Flask(__name__)
    
def classify_query(user_message, ai):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert assistant in Astronomy and Virtual Observatories. "
                "Analyze the user's query and respond with a JSON object that includes the resource category (category, which can be SIA for images, SSA for spectra, SCS for object search, SLA for spectral lines, or REGISTRY for service discovery) "
                "and a list of names or identifiers for the astronomical object (object, including SIMBAD designations such as Messier numbers, NGC/IC numbers, common names, or other catalog identifiers). "
                "If no object is mentioned, return an empty list; if the query is not related to a specific object, return a random object from SIMBAD. "
                "Additionally, include title (dataset or image title), format (file format), instrument (instrument used), posAR (Right Ascension coordinates), posDEC (Declination coordinates), bandpass (band used in the observation), and server (specific IVOA server if required if the user say that). If no applicable information is available, return 'none. "
                "Respond only with the JSON object, without explanations."
            ),
        },
        {"role": "user", "content": user_message},
    ]
    if ai == "openai":
        response = gpt_client.get_chat_completion(messages)
    elif ai == "deepseek":
        response = deepseek_client.get_chat_completion(messages)
    else:
        raise ValueError("El parámetro 'ai' debe ser 'openai' o 'deepseek'")
    
    response_text = response["choices"][0]["message"]["content"]
    response_text = response_text.replace("```json", "").replace("```", "")
    # Convertir a diccionario (cuidado: eval puede ser peligroso; se recomienda usar json.loads si la respuesta es JSON válido)
    response_json = eval(response_text)
    return response_json

def coordinate_resolver_vizier(object_names):
    """
    Resuelve las coordenadas (RA, Dec) de un objeto usando VizieR.
    Devuelve las coordenadas en formato decimal compatible con IVOA.
    """
    viz = Vizier(columns=["RAJ2000", "DEJ2000"])
    result = viz.query_object(object_names[0])
    
    if result:
        result_table = result[0]
        if "RAJ2000" in result_table.colnames and "DEJ2000" in result_table.colnames:
            ra = result_table["RAJ2000"][0]
            dec = result_table["DEJ2000"][0]
            
            # Convertir a formato decimal estándar IVOA
            coords = SkyCoord(ra, dec, unit=(u.deg, u.deg), frame='icrs')
            return coords.ra.degree, coords.dec.degree
    
    return None

def sia(coordinates, classification, size=0.01, max_size=10.0):
    ra, dec = coordinates
    format = classification.get("format")
    bandpass = classification.get("bandpass")
    instrument = classification.get("instrument")
    
    print(f"🔭 Buscando imágenes en SIA para ({ra}, {dec})")
    sia_services = list(pyvo.registry.search(servicetype="sia"))
    
    if not sia_services:
        return "No se encontraron servicios SIA disponibles."

    random.shuffle(sia_services)
    
    while size <= max_size:
        for service in sia_services:
            try:
                sia_service = pyvo.dal.SIAService(service.access_url)
                images = sia_service.search(pos=(ra, dec), size=size)

                if len(images) > 0:
                    random_image = random.choice(images)
                    image_url = random_image.getdataurl()
                    response = requests.get(image_url)
                    
                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content))
                        img.show()
                        print(f"📏 Tamaño óptimo encontrado: {size} grados")
                        return image_url
                
            except Exception as e:
                print(f"Error al consultar {service.access_url}: {e}")

        size *= 2  # Duplicar el tamaño si no se encuentra nada
        print(f"🔄 Aumentando tamaño de búsqueda a {size} grados...")
    
    return "No se encontraron imágenes en ningún servicio SIA."

@app.route("/execute", methods=["POST"])
def execute():
    try:
        data = request.get_json()
        user_message = data.get("code")
        ai = data.get("ai")
        if not user_message:
            return jsonify({"error": "No se recibió un mensaje válido."}), 400

        # Clasificar la consulta
        classification = classify_query(user_message, ai)
        print("Classification:", classification)
        category = classification.get("category")
        object_name = classification.get("object")

        if category is None:
            return jsonify({"error": "No se pudo clasificar la consulta."}), 400

        elif category == "SIA":
            if classification.get("posAR") != "none" and classification.get("posDEC") != "none":
                coordinates = classification.get("posAR"), classification.get("posDEC")
                # Convertir a formato decimal estándar IVOA
                coordinates = SkyCoord(coordinates[0], coordinates[1], unit=(u.deg, u.deg), frame='icrs')
                coordinates = coordinates.ra.degree, coordinates.dec.degree
            else:
                print("Resolviendo coordenadas de", object_name)
                coordinates = coordinate_resolver_vizier(object_name)
            
            print("Coordinates:", coordinates)

            response = sia(coordinates,classification)

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
