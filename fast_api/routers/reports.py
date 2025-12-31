from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from fast_api.app.core.database import get_db
from fast_api.schemas.reports import ReportsResponse

router = APIRouter( prefix = "/reports", tags = ["Reports"] )

@router.get("/",response_model = ReportsResponse)
def get_reports(db: Session = Depends(get_db)):

    # Django table name is `reports_report`; query that table instead of `reports`
    rows = db.execute(text("SELECT report_id, title FROM reports_report")).fetchall()
    return {
        "reports": [      
        {"report_id": r[0], "title": r[1]}
        for r in rows
        ]
    }  