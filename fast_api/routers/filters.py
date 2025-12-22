from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db

router = APIRouter(prefix="/filters", tags=["Filters"])

@router.get("/{report_id}")

def get_filters(report_id: int, db:Session = Depends(get_db)):
    
    rows = db.execute(text("""
                        SELECT f.filter_label, f.column_name, f.allowed_values,f.default values
                           FROM reports.filter f
                           JOIN reports_report r ON f.report_id = r.id
                           wHERE r.id = :report_id
"""),
{report_id:report_id}).fetchall()
    
    return {"filters": [
        { 
            "filter_label":r[0],
            "column_name":r[1],
            "allowed_values":r[2],
            "default_values":r[3]
            
            }
            for r in rows
        ]}