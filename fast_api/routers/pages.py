from fastapi import APIRouter
router = APIRouter()
@router.get("/pages")
def get_pages(report_id: int):
    return {"pages": [{ 

                       "Διακριτικά συντονιζόμενη Ε&Α",
                       "Κοινωνικοοικονομικός Στόχος",
                       "Σχήμα Χρηματοδότησης",
                       "Βασικοί Δείκτες"

                       }]
            }  