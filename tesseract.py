import pytesseract
from PIL import Image


def tess(img, lang):
    img = Image.open(img)
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    text = pytesseract.image_to_string(img, lang=lang).strip()
    return text
