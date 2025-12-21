from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from api.core.database import get_db

router = APIRouter( prefix = "/reports", tags = ["Reports"] )

@router.get("/")
def get_reports(db: Session = Depends(get_db)):

    rows = db.execute(text("SELECT report_if,title FROM reports")).fetchall()
    return {
        "reports": [      
        {"report_id": r[0], "title": r[1]}
        for r in rows
        ]
    }  