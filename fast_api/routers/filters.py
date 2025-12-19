from fastapi import APIRouter
router = APIRouter()
@router.get("/filters")
def get_filters(report_id: int):
    return {"filters": [{ "column_name": "Year"}]}