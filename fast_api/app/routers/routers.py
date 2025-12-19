from fastapi import APIRouter
router = APIRouter()
@router.get("/reports")
def get_reports():
    return {"reports": [{"report_id": "gbard-landing(1)", "title": "GBARD Landing Page"}]}  # Placeholder for actual report data