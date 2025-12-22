from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db

router = APIRouter(prefix="/pages", tags=["Pages"])
@router.get("/{report_id}")

def get_pages(report_id: int, db: Session = Depends(get_db)):
    
    
    rows = db.execute(text("""
                      SELECT p.page_name, p.page_id, p.is_default from reports_pages p 
                      JOIN reports_report r ON p.report_id = r.id
                      WHERE r.id =:report_id
                      ORDER BY p."order"
    """),
    {"report_id":report_id}).fetchall()
    
    return {
        "pages": [ 

                         {
                             "page_name": r[0],
                                "page_id": r[1],
                                "is_default": r[2]
                         }
                            for r in rows
                       ]
   
            } 