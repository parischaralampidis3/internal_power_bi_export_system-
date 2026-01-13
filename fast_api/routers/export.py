from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from fast_api.app.core.database import get_db

router = APIRouter( prefix = "/export", tags = ["Export"])

@router.post("/preview", status_code=200)

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
    
    report_pk, iframe_url = report
        
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
    

@router.post("/run", status_code=200)
def export_run(payload: dict, db: Session = Depends(get_db)):
    report_id = payload.get("report_id")
    page_id = payload.get("page_id")
    filters = payload.get("filters", {})

    if not report_id or not page_id:
        raise HTTPException(status_code=400, detail="report_id and page_id are required.")

    # Validate report
    report = db.execute(
        text("SELECT id, iframe_url FROM reports_report WHERE report_id = :rid"),
        {"rid": report_id}
    ).fetchone()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")
    report_pk, iframe_url = report

    # Validate page
    page_obj = Pages.objects.filter(report_id=report_pk, page_id=page_id).first()
    if not page_obj:
        raise HTTPException(status_code=404, detail="Page not found for this report.")
    if not page_obj.powerbi_page_name:
        raise HTTPException(status_code=404, detail="Power BI page name not set for this page.")
    powerbi_page_name = page_obj.powerbi_page_name

    # Validate filters
    rows = db.execute(
        text("SELECT column_name, allowed_values FROM reports_filter WHERE report_id = :pk"),
        {"pk": report_pk}
    ).fetchall()
    allowed_filters = {r[0]: r[1] for r in rows}
    for k, v in filters.items():
        if k in allowed_filters and str(v) not in allowed_filters[k]:
            raise HTTPException(status_code=400, detail=f"Invalid value for filter {k}")

    # Export PNG
    output_file = f"exports/{report_id}_{page_id}.png"
    export_png_from_iframe(iframe_url=iframe_url, output_path=output_file)

    return {
        "message": "Export Completed Successfully",
        "file": output_file,
        "powerbi_page_name": powerbi_page_name,
        "report_id": report_id,
        "page_id": page_id,
        "filters": filters
    }