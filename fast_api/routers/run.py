from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fast_api.app.core.database import get_db
from fast_api.app.utils.export_png import export_png_from_iframe

# Django models (Django is already set up in main.py)
from reports.models import Pages

router = APIRouter(prefix="/export", tags=["Export"])

@router.post("/run", status_code=200)
def export_run(payload: dict, db: Session = Depends(get_db)):
    report_id = payload.get("report_id")
    page_id = payload.get("page_id")
    filters = payload.get("filters", {})

    if not report_id or not page_id:
        raise HTTPException(status_code=400, detail="report_id and page_id are required.")

    report = db.execute(
        "SELECT id, iframe_url FROM reports_report WHERE report_id = :rid",
        {"rid": report_id}
    ).fetchone()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")

    report_pk, iframe_url = report

    page_obj = Pages.objects.filter(report_id=report_pk, page_id=page_id).first()
    if not page_obj:
        raise HTTPException(status_code=404, detail="Page not found for this report.")
    if not page_obj.powerbi_page_name:
        raise HTTPException(status_code=404, detail="Power BI page name not set for this page.")

    powerbi_page_name = page_obj.powerbi_page_name

    # Validate filters
    rows = db.execute(
        "SELECT column_name, allowed_values FROM reports_filter WHERE report_id = :pk",
        {"pk": report_pk}
    ).fetchall()
    allowed_filters = {r[0]: r[1] for r in rows}
    for k, v in filters.items():
        if k in allowed_filters and str(v) not in allowed_filters[k]:
            raise HTTPException(status_code=400, detail=f"Invalid value for filter {k}")

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
