from pydantic import BaseModel
from typing import List

class PageOut(BaseModel):
    page_id : str
    page_name: str
    is_default: bool

class PagesResponse(BaseModel):
    pages: list[PageOut]