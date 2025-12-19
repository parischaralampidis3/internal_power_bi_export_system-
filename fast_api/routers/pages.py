from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.models import Pages

router = APIRouter()

@router.get("/pages")
def get_pages(report_id: int, db: Session = Depends(get_db)):
    """Get all pages for a specific report"""
    pages = (
        db.query(Pages)
        .filter(Pages.report_id == report_id)
        .order_by(Pages.order)
        .all()
    )

    return {
        "pages": [
            {
                "id": p.id,
                "page_name": p.page_name,
                "page_id": p.page_id,
                "order": p.order,
                "is_default": p.is_default,
                "thumbnail_url": p.thumbnail_url,
            }
            for p in pages
        ]
    }