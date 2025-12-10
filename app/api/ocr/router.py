from typing import Annotated
import aiofiles

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session

from app.core.database import get_session

from .schemas import OCRReadSuccess, OCRReadOther, OCRCreate
from .services import process_ocr_document
from .models import OCRStatus, OCRResult


ocr_router = APIRouter()


########################################################################################################################
@ocr_router.get("/get-ocr-status/{ocr_id}")
async def get_status(ocr_id: int, session: Annotated[Session, Depends(get_session)]) -> OCRReadSuccess | OCRReadOther:
    result = session.get(OCRResult, ocr_id)

    if result is None:
        raise HTTPException(status_code=404, detail=f"OCR Result with ID {ocr_id} not found")

    if result.status == OCRStatus.COMPLETED:
        return OCRReadSuccess(
            id=result.id,
            status=result.status.value,
            title=result.title,
            date=result.date,
            code=result.code,
        )
    elif result.status == OCRStatus.FAILED:
        return OCRReadOther(id=result.id, status=result.status.value, error=result.error)
    else:
        return OCRReadOther(id=result.id, status=result.status.value)


########################################################################################################################
@ocr_router.post("/post-ocr-file")
async def post_file(session: Annotated[Session, Depends(get_session)], file: UploadFile = File(...)) -> OCRCreate:
    new_ocr = OCRResult(
        status=OCRStatus.PENDING.value
    )
    session.add(new_ocr)
    session.commit()
    session.refresh(new_ocr)

    file_location = f"uploads/{new_ocr.id}.jpg"
    async with aiofiles.open(file_location, "wb") as file_object:
        content = await file.read()
        await file_object.write(content)

    process_ocr_document.delay(new_ocr.id)

    return OCRCreate(id=new_ocr.id, status=new_ocr.status.value)
