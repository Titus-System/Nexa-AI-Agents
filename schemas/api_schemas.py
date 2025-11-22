from typing import Any, Dict, Optional
from pydantic import BaseModel


class SingleClassificationRequest(BaseModel):
    progress_channel: str
    partnumber: str
    description: Optional[str] = None
    manufacturer: Optional[str] = None
    supplier: Optional[str] = None

class BatchClassificationRequest(BaseModel):
    progress_channel: str
    partnumbers: Dict[str, Any]


class SingleClassification(BaseModel):
    partnumber: Optional[str] = None
    ncm : Optional[str] = None
    description : Optional[str] = None
    exception : Optional[str] = None
    nve : Optional[str] = None
    fabricante : Optional[str] = None
    endereco : Optional[str] = None
    pais : Optional[str] = None
    confidence_score: Optional[float] = None


class DoneProcessing(BaseModel):
    status: str = 'done'
    job_id: Optional[str] = None
    result: SingleClassification


class ProgressSchema(BaseModel):
    current: int
    total: int
    message: Optional[str] = None


class UpdateProgressStatus(BaseModel):
    status: str = 'processing'
    job_id: Optional[str] = None
    progress: ProgressSchema


class PartialResult(BaseModel):
    status:str = "partial_result"
    job_id: Optional[str] = None
    current: int
    total: int
    message: str
    single_classification: SingleClassification


class FailedProcessing(BaseModel):
    status: str = "failed"
    job_id: Optional[str] = None
    error: Optional[str] = None