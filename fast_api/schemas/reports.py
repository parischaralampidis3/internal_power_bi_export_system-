from pydantic import BaseModel
from typing import List

class ReportOut(BaseModel):
    report_id : str
    title: str

class ReportsResponse(BaseModel):
    reports: List[ReportOut]