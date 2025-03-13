# importar las 11brerias pyvo y matploti1b 
from pyvo.dal import tap
from matplotlib import pyplot as plt


#URL del servicio TAP
tap_url = "http://dc.zah.uni-heidelberg.de/tap"

# Crear una conexión con el servicio TAP
service = tap.TAPService(tap_url)

#Construir la consulta
query = """
SELECT access_url
FROM ivoa.obscore
WHERE target_name = 'Jupiter'
AND dataproduct_type = 'image'
"""

# Ejecutar la consulta
result = service.search(query)

#Obtener la URL de le inegen de Jüpiter
if len(result) > 0:
    access_url = result[ 'access_url'][0]
    print("URL de la imagen de Júpiter:", access_url)
else:
    print("no se encontraron imágenes de Júpiter en el espectro visible.")