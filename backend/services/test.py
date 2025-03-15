import pyvo
import matplotlib.pyplot as plt
from astropy.io import fits

# Definir coordenadas del objeto a buscar (por ejemplo, M42 - Nebulosa de Orión)
ra = 83.8221   # Ascensión recta en grados
dec = -5.3911  # Declinación en grados
size = 0.2     # Tamaño del recorte en grados

# URL del servicio SIAP (Simple Image Access Protocol) de SkyView
siap_service = "https://skyview.gsfc.nasa.gov/cgi-bin/vo/sia.pl?"

# Crear la consulta al servicio SIAP
service = pyvo.dal.SIAService(siap_service)
result = service.search(pos=(ra, dec), size=size, format="image/fits")

# Obtener la URL de la primera imagen disponible
image_url = result[0].getdataurl()

# Descargar la imagen FITS
fits_file = fits.open(image_url)
image_data = fits_file[0].data

# Mostrar la imagen
plt.figure(figsize=(8, 8))
plt.imshow(image_data, cmap='gray', origin='lower')
plt.colorbar(label="Intensidad")
plt.title("Imagen DSS de M42 (Nebulosa de Orión)")
plt.show()
