import io
import base64
from pdfminer.high_level import extract_text as pdfminer_extract_text
from pdf2image import convert_from_bytes
from PIL import Image


def extract_text_from_pdf(pdf_stream):
    """Extrae texto de un archivo PDF en memoria usando pdfminer y lo devuelve como una cadena UTF-8."""
    pdf_stream.seek(0)  # Asegurarse de reiniciar el puntero
    text = pdfminer_extract_text(pdf_stream)
    return text.encode('utf-8').decode('utf-8') if text else None


def extract_images_from_pdf(pdf_stream):
    """Extrae imágenes de un archivo PDF en memoria y las devuelve como un array de cadenas base64."""
    images = []
    pdf_stream.seek(0)  # Reiniciar el puntero al inicio del archivo en memoria
    pages = convert_from_bytes(pdf_stream.read())  # Convertir el PDF a imágenes en bytes
    for page in pages:
        buffer = io.BytesIO()
        page.save(buffer, format="PNG")
        image_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        images.append(image_str)
    return images


def process_pdf(pdf_file):
    """Procesa el PDF recibido en un archivo en memoria, extrayendo texto y buscando imágenes."""
    pdf_stream = io.BytesIO(pdf_file.read())  # Crear un stream en memoria desde el archivo PDF
    text = extract_text_from_pdf(pdf_stream)
    images = extract_images_from_pdf(pdf_stream)
    
    return text, images
