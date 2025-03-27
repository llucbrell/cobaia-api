import io
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from markdownify import markdownify as md

def extract_html_from_pdf(pdf_stream):
    """Extrae contenido del PDF como HTML usando pdfminer."""
    pdf_stream.seek(0)
    output = io.StringIO()  # Cambiar a StringIO para salida de texto
    laparams = LAParams()
    extract_text_to_fp(pdf_stream, output, laparams=laparams, output_type='html', codec=None)  # Eliminar codec
    return output.getvalue()

def pdf_to_markdown_with_structure(pdf_file):
    """Convierte un archivo PDF en memoria a formato Markdown preservando la estructura."""
    pdf_stream = io.BytesIO(pdf_file.read())  # Crear un stream en memoria desde el archivo PDF
    
    # Extraer contenido del PDF como HTML
    html_content = extract_html_from_pdf(pdf_stream)
    
    # Convertir HTML a Markdown usando markdownify
    markdown_content = md(html_content, heading_style="ATX")  # Usa estilo de encabezado ATX (### Header)
    
    return markdown_content

