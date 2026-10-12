
from io import BytesIO

import pytesseract
import streamlit as st
from PIL import Image
from pypdf import PdfReader


def extract_report_text(uploaded_file):
    """Extract text from a PDF or image medical report."""
    filename = uploaded_file.name.lower()
    file_bytes = uploaded_file.getvalue()

    if filename.endswith(".pdf"):
        reader = PdfReader(BytesIO(file_bytes))
        pages = [
            page.extract_text() or ""
            for page in reader.pages
        ]
        text = "\n\n".join(pages).strip()

        if text:
            return text

        st.warning(
            "This PDF contains no selectable text. "
            "Scanned PDF OCR will be added next."
        )
        return ""

    if filename.endswith((".png", ".jpg", ".jpeg")):
        image = Image.open(BytesIO(file_bytes)).convert("RGB")
        return pytesseract.image_to_string(image).strip()

    raise ValueError("Unsupported file format.")
