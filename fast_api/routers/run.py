from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from fast_api.app.core.database import get_db

router = APIRouter( prefix = '/run', tags=['Run'] )

router.post('/run', status_code=200)
