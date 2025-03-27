from pdf2image import convert_from_path
import os
import base64
import io
from PIL import Image



def convert_pdf_to_images(pdf_file):
    """
    Convierte un archivo PDF en memoria a una lista de imágenes en formato base64.
    """
    images = convert_from_bytes(pdf_file.read())  # Convertir cada página en una imagen
    image_list = []

    for image in images:
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        image_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        image_list.append(image_b64)

    return image_list

# Function to convert PDF pages to images and save them
def save_pdf_pages_as_jpg(pdf_path, output_folder='uploads'):
    """
    Convierte cada página de un archivo PDF a una imagen JPG y la guarda en el directorio 'uploads'.
    """
    # Asegurarse de que el directorio existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convertir cada página en una imagen
    images = convert_from_path(pdf_path)

    # Lista para almacenar las rutas de las imágenes
    image_paths = []

    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'page_{i + 1}.jpg')
        image.save(image_path, format="JPEG")
        image_paths.append(image_path)

    return image_paths