import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

# Tesseract location
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Poppler location
POPPLER_PATH = (
    r"C:\poppler\Library\bin"
)


def extract_text_from_image(image_path):

    try:

        image = Image.open(image_path)

        text = pytesseract.image_to_string(
            image,
            lang="eng"
        )

        return text

    except Exception as e:

        print(
            f"OCR failed: {image_path}"
        )

        print(e)

        return ""


def extract_text_from_pdf_images(pdf_path):

    all_text = ""

    try:

        pages = convert_from_path(
            pdf_path,
            poppler_path=POPPLER_PATH
        )

        for page in pages:

            text = pytesseract.image_to_string(
                page,
                lang="eng"
            )

            all_text += "\n" + text

    except Exception as e:

        print(
            f"PDF OCR failed: {pdf_path}"
        )

        print(e)

    return all_text