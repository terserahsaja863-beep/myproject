from __future__ import annotations

from io import BytesIO

import numpy as np
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def image_to_jpg_bytes(image: np.ndarray) -> bytes:
    """Encode an RGB numpy image as downloadable JPG bytes."""
    buffer = BytesIO()
    Image.fromarray(image).save(buffer, format="JPEG", quality=95)
    return buffer.getvalue()


def image_to_pdf_bytes(image: np.ndarray) -> bytes:
    """Place an RGB numpy image on an A4 PDF page and return PDF bytes."""
    image_buffer = BytesIO()
    Image.fromarray(image).save(image_buffer, format="PNG")
    image_buffer.seek(0)
    pdf_buffer = BytesIO()
    page_width, page_height = A4
    pdf = canvas.Canvas(pdf_buffer, pagesize=A4)
    reader = ImageReader(image_buffer)
    img_width, img_height = reader.getSize()
    scale = min((page_width - 48) / img_width, (page_height - 48) / img_height)
    draw_width = img_width * scale
    draw_height = img_height * scale
    x = (page_width - draw_width) / 2
    y = (page_height - draw_height) / 2
    pdf.drawImage(reader, x, y, width=draw_width, height=draw_height, preserveAspectRatio=True)
    pdf.showPage()
    pdf.save()
    return pdf_buffer.getvalue()
