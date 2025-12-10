from enum import Enum

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Enum as SQLEnum


class OCRStatus(Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class OCRResult(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    title: str | None = None
    date: str | None = None
    code: str | None = None

    status: OCRStatus = Field(sa_column=Column(SQLEnum(OCRStatus), default=OCRStatus.PENDING.value, nullable=False))
    error: str | None = None
