from pydantic import BaseModel
from typing import List,Any,Optional

class FilterOut(BaseModel):
    filter_id : str
    filter_name: List[Any]
    filter_type: Optional[str]

class FiltersResponse(BaseModel):
    filters: List[FilterOut]