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

    if not report_id or not page_id:
        raise HTTPException(
            status_code=400, 
            detail="report_id and page_id are required."
            )  
    
    report = db.execute(
             text("""
                  SELECT id, iframe_url 
                  FROM reports_report 
                  WHERE report_id = :rid
                  """), 
                  {"rid": report_id}
                  ).fetchone()


    if not report:
        raise HTTPException(
            status_code=404, 
            detail = "Report not found"
            )
        
    # Validate page belongs to report

    page = db.execute(
            text(""" 
                 SELECT page_id 
                FROM reports_pages
                WHERE report_id = :pk AND page_id = :page 
                 """), 
                {"pk": report_pk, "page": page_id}
                ).fetchone()
    
    if not page:
        raise HTTPException(
            status_code = 404, 
            detail = "Page not found for this report."
            )

    #validate load allowed filter values

    rows = db.execute(
             text(""" 
            SELECT column_name, allowed_values
            FROM reports_filter
            WHERE report_id = :pk
            """),
            {"pk": report_pk}
            ).fetchall()
    
    allowed_filters = {r[0]: r[1] for r in rows}

    return {
        "message": "Preview validation passed",
        "iframe_url": iframe_url,
        "allowed_filters": allowed_filters
    }
    

