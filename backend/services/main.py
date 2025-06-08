from flask import Flask, request, jsonify
from dotenv import load_dotenv
import pyvo
from astroquery.vizier import Vizier
import requests
from PIL import Image
from io import BytesIO
import random
from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.io import fits
import matplotlib
matplotlib.use('Agg')  # Usa backend no-interactivo
import matplotlib.pyplot as plt
import numpy as np
import tempfile
import os

def plot_fits_image_from_url(fits_url, output_path="imagen_fits.png"):
    try:
        # Descargar el archivo FITS temporalmente
        response = requests.get(fits_url)
        response.raise_for_status()  # Lanza error si hubo problemas al descargar

        with tempfile.NamedTemporaryFile(delete=False, suffix=".fits") as tmp_file:
            tmp_file.write(response.content)
            temp_fits_path = tmp_file.name

        # Abrir archivo FITS
        with fits.open(temp_fits_path) as hdul:
            hdul.info()

            # Buscar la primera extensión que contenga datos tipo imagen
            image_data = None
            for hdu in hdul:
                if hdu.data is not None:
                    image_data = hdu.data
                    break

            if image_data is None:
                raise ValueError("No se encontró una imagen en el archivo FITS.")

            # Graficar y guardar la imagen
            plt.figure(figsize=(8, 8))
            plt.imshow(image_data, cmap='gray', origin='lower')
            plt.colorbar()
            plt.title("Imagen FITS")
            plt.savefig(output_path, bbox_inches="tight")
            plt.close()

            print(f"✅ Imagen guardada en: {output_path}")

        # Eliminar archivo temporal
        os.remove(temp_fits_path)

    except Exception as e:
        print(f"❌ Error: {e}")


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


def improve_sia_search(ra, dec, size, format, bandpass, instrument, ai):
    """ Utiliza IA para mejorar los parámetros de búsqueda en SIA """
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert in astronomy data retrieval. Given the following parameters for a SIA query (IVOA), "
                "optimize them to increase the chance of finding an image."
                "Respond with a JSON containing 'size' (recommended search size in degrees), 'bandpass' (suggested alternative if none is found), "
                "and 'priority_services' (a list of recommended SIA service URLs)."
                "searching for images in the specified format, bandpass, and instrument."
                "respond just with the JSON object, without explanations."

            ),
        },
        {
            "role": "user",
            "content": f"RA: {ra}, DEC: {dec}, size: {size}, format: {format}, bandpass: {bandpass}, instrument: {instrument}",
        },
    ]
    if ai == "openai":
        response2 = gpt_client.get_chat_completion(messages)
    elif ai == "deepseek":
        response2 = deepseek_client.get_chat_completion(messages)
    else:
        raise ValueError("El parámetro 'ai' debe ser 'openai' o 'deepseek'")

    response_text = response2["choices"][0]["message"]["content"]
    print(response_text)
    response_text = response_text.replace("```json", "").replace("```", "")
    response_json = eval(response_text)  # Se recomienda usar json.loads() si el JSON es seguro.
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

def sia(coordinates, classification, size, ai):
    ra, dec = coordinates
    format = classification.get("format")
    bandpass = classification.get("bandpass")
    instrument = classification.get("instrument")

    # Mejorar parámetros de búsqueda con IA
    optimized_params = improve_sia_search(ra, dec, size, format, bandpass, instrument, ai)
    size = optimized_params.get("size", size)
    bandpass = optimized_params.get("bandpass", bandpass)
    priority_services = optimized_params.get("priority_services", [])

    print(f"🔭 Buscando imágenes en SIA para ({ra}, {dec}) con tamaño {size}° y banda {bandpass}")

    sia_services = list(pyvo.registry.search(servicetype="sia"))

    if priority_services:
        sia_services = [s for s in sia_services if s.access_url in priority_services] + sia_services

    if not sia_services:
        return "No se encontraron servicios SIA disponibles."

    random.shuffle(sia_services)
    
    for service in sia_services:
        try:
            sia_service = pyvo.dal.SIAService(service.access_url)
            images = sia_service.search(pos=(ra, dec), size=size, band=bandpass)

            if len(images) > 0:
                valid_images = [img for img in images if img["format"].startswith("image/")]

                if valid_images:
                    random_image = random.choice(valid_images)
                    image_url = random_image.getdataurl()
                    response = requests.get(image_url)

                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content))
                        img.show()
                        plot_fits_image_from_url(image_url)
                        print(f"Imagen descargada y mostrada: {image_url}")
                        return image_url
                    else:
                        print(f"Error al descargar la imagen: {response.status_code}")
                else:
                    print(f"No se encontraron imágenes válidas en el servicio {service.access_url}.")
        except Exception as e:
            print(f"Error al consultar {service.access_url}: {e}")

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

            response = sia(coordinates, classification, size=0.01 , ai = ai)

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
