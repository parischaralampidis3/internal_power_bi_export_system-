from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from fast_api.app.core.database import get_db
from fast_api.schemas.pages import PagesResponse

router = APIRouter(prefix="/pages", tags=["Pages"])
@router.get("/{report_id}",response_model = PagesResponse )

def get_pages(report_id: str, db: Session = Depends(get_db)):
    
    
    rows = db.execute(text("""
                      SELECT p.page_name, p.page_id, p.is_default from reports_pages p 
                      JOIN reports_report r ON p.report_id = r.id
                      WHERE r.report_id =:report_id
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