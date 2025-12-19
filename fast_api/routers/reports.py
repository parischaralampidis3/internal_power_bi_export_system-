from fastapi import APIRouter
router = APIRouter()
@router.get("/reports")
def get_reports(report_id: int):
    return {"reports": [{

        "report_id": "1", 
        "title": "GBARD Landing Page"

        }]
    }  