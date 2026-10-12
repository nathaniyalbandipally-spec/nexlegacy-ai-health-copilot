
from io import BytesIO

import pytesseract
from PIL import Image
from pypdf import PdfReader
from pdf2image import convert_from_bytes


def extract_report_text(uploaded_file):
    """Extract text from PDFs and medical report images."""
    filename = uploaded_file.name.lower()
    file_bytes = uploaded_file.getvalue()

    if filename.endswith(".pdf"):
        reader = PdfReader(BytesIO(file_bytes))
        pages_text = [
            page.extract_text() or ""
            for page in reader.pages
        ]
        text = "\n\n".join(pages_text).strip()

        if len(text) >= 20:
            return text

        # Scanned PDF: convert pages to images and use OCR.
        images = convert_from_bytes(
            file_bytes,
            dpi=200,
            first_page=1,
            last_page=min(len(reader.pages), 10)
        )

        text = "\n\n".join(
            pytesseract.image_to_string(image)
            for image in images
        ).strip()

        return text

    if filename.endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(BytesIO(file_bytes)).convert("RGB")
        return pytesseract.image_to_string(image).strip()

    raise ValueError("Unsupported file format.")
