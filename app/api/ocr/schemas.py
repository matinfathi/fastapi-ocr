from pydantic import BaseModel


class OCRReadSuccess(BaseModel):
    id: int
    status: str
    title: str
    date: str
    code: str


class OCRReadOther(BaseModel):
    id: int
    status: str
    error: str | None = None


class OCRCreate(BaseModel):
    id: int
    status: str
