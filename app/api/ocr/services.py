import pytesseract
from PIL import Image
from gliner import GLiNER

from sqlmodel import Session

from app.core.database import engine
from app.core.celery_config import celery_app
from .models import OCRResult, OCRStatus


def read_image(image_path: str) -> Image.Image | str:
    return Image.open(image_path)


def image2text(image: Image.Image) -> str:
    return pytesseract.image_to_string(image)


def ocr(image_path: str) -> str:
    try:
        image = read_image(image_path)
        text = image2text(image)
        return text
    except Exception as e:
        return f"Error during OCR process: {e}"


def ner(input_text: str) -> dict[str, str]:
    result = {}
    model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")
    labels = ["date", "title", "code"]

    entities = model.predict_entities(input_text, labels)

    for entity in entities:
        result[entity["label"]] = entity["text"]

    if all(key in result for key in labels):
        return result
    else:
        raise Exception("NER failed to extract all required entities")


@celery_app.task
def process_ocr_document(ocr_id: int):
    with Session(engine) as session:
        result = session.get(OCRResult, ocr_id)
        if not result:
            raise Exception(f"OCR Result with ID {ocr_id} not found")

        try:
            result.status = OCRStatus.PROCESSING

            session.add(result)
            session.commit()
            # OCR ---------------------------
            image_path = f"uploads/{result.id}.jpg"
            extracted_text = ocr(image_path)
            # -------------------------------

            # NER ---------------------------
            ner_result = ner(extracted_text)
            # ner_result = {"code": "123", "title": "test", "date": "12/12/12"}
            # -------------------------------

            result.status = OCRStatus.COMPLETED
            result.code = ner_result["code"]
            result.title = ner_result["title"]
            result.date = ner_result["date"]

            session.add(result)
            session.commit()

        except Exception as e:
            result.status = OCRStatus.FAILED
            result.error = str(e)
            session.add(result)
            session.commit()
