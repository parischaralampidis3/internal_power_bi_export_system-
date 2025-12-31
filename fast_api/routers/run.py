from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from fast_api.app.core.database import get_db

router = APIRouter( prefix = '/run', tags=['Run'] )

router.post('/run', status_code=200)

def export_run(payload: dict, db: Session = Depends(get_db)):

    report_id = payload.get("report_id")
    page_id = payload.get("page_id")
    filters = payload.get("filters",{})

    if not report_id or not page_id:
        raise HTTPException(
            status_code = 400,
            detail = "eport_id and page_id are required."
        )
    

    #validate report exists

    report = db.execute(text("""

              """))