from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db

router = APIRouter( prefix = "/export", tags = ["Export"])

@router.post("/preview", status_code=202)

def export_preview(payload: dict, db: Session = Depends(get_db)):

    report_id = payload.get("report_id")
    page_id = payload.get("page_id")
    filters = payload.get("filters",{})

