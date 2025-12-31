from fastapi import FastAPI

from fast_api.routers.reports import router as reports_router
from fast_api.routers.pages import router as pages_router
from fast_api.routers.filters import router as filters_router
from fast_api.routers.export import router as export_router

app = FastAPI(title="Reports API", version="1.0.0")
app.include_router(reports_router, prefix="/api")
app.include_router(pages_router, prefix="/api")
app.include_router(filters_router, prefix="/api")  
app.include_router(export_router, prefix="/api") 

@app.get("/")
def read_root():
    return {"Hello": "World"}