from typing import Optional
from pydantic import BaseModel


class SingleClassificationRequest(BaseModel):
    progress_channel: str
    partnumber: str
    description: Optional[str] = None
    manufacturer: Optional[str] = None
    supplier: Optional[str] = None


class SingleClassification(BaseModel):
    ncm : Optional[str] = None
    description : Optional[str] = None
    exception : Optional[str] = None
    nve : Optional[str] = None
    fabricante : Optional[str] = None
    endereco : Optional[str] = None
    pais : Optional[str] = None
    confidence_score: Optional[float]


class DoneProcessing(BaseModel):
    status: str = 'done'
    result: SingleClassification


class ProgressSchema(BaseModel):
    current: int
    total: int
    message: Optional[str] = None


class UpdateProgressStatus(BaseModel):
    status: str = 'processing'
    progress: ProgressSchema


class FailedProcessing(BaseModel):
    status: str = "failed"
    error: Optional[str] = None