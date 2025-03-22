import pyvo
import random
import requests
from PIL import Image
from io import BytesIO

def obtener_imagen_sia(ra, dec, size=0.1):
    # Buscar todos los servicios SIA disponibles y convertirlos en lista
    sia_services = list(pyvo.registry.search(servicetype="sia"))

    for service in sia_services[:5]:  # Mostrar solo los primeros 5 servicios
        print(f"   📡 URL: {service.access_url}")
        print(f"   🎨 Formatos: {service.content_types}")
        print(f"   🌍 Bandas: {service.waveband}")
        print(f"   🏢 Publicado por: {getattr(service, 'creator_seq', 'Desconocido')}")
        print("-" * 50)

    # Verificar si hay servicios disponibles
    if not sia_services:
        print("No se encontraron servicios SIA disponibles.")
        return

    # Mezclar los servicios para elegir en orden aleatorio
    random.shuffle(sia_services)

    for service in sia_services:
        sia_service_url = service.access_url
        print(f"Intentando con servicio SIA: {sia_service_url}")

        try:
            # Conectar al servicio SIA
            sia_service = pyvo.dal.SIAService(sia_service_url)
            
            # Realizar la consulta en la posición dada
            images = sia_service.search(pos=(ra, dec), size=size)

            if len(images) > 0:
                # Elegir una imagen aleatoria de los resultados
                random_image = random.choice(images)
                image_url = random_image.getdataurl()
                print(f"Imagen encontrada: {image_url}")

                # Descargar la imagen
                response = requests.get(image_url)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    img.show()  # Muestra la imagen
                    return  # Termina la función si encuentra una imagen
                else:
                    print("Error al descargar la imagen.")

        except Exception as e:
            print(f"Error al consultar {sia_service_url}: {e}")

    print("No se encontraron imágenes en ningún servicio SIA.")

# Coordenadas de búsqueda (ejemplo: Nebulosa de Orión)
ra, dec = 83.8221, -5.3911
obtener_imagen_sia(ra, dec)
