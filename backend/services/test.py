from astropy.io import fits
import matplotlib.pyplot as plt

# Abrir el archivo FITS desde una URL
hdul = fits.open("https://irsa.ipac.caltech.edu:443/cgi-bin/2MASS/IM/nph-im?ds=asky&atdir=/ti02&dh=991229s&scan=028&name=ji0280221.fits")

# Mostrar información general del archivo
hdul.info()

# Acceder a los datos de la primera extensión (extensión 0 o 1 dependiendo del FITS)
image_data = hdul[0].data  # O puede que sea hdul[1].data, si hdul[0] no contiene imagen

# Visualizar la imagen
plt.figure(figsize=(8, 8))
plt.imshow(image_data, cmap='gray', origin='lower')
plt.colorbar()
plt.title("Imagen FITS")
plt.show()

# Cerrar el archivo después de usarlo
hdul.close()
