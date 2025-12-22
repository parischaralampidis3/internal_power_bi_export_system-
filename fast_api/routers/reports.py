from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db

router = APIRouter( prefix = "/reports", tags = ["Reports"] )

@router.get("/")
def get_reports(db: Session = Depends(get_db)):

    # Django table name is `reports_report`; query that table instead of `reports`
    rows = db.execute(text("SELECT report_id, title FROM reports_report")).fetchall()
    return {
        "reports": [      
        {"report_id": r[0], "title": r[1]}
        for r in rows
        ]
    }  