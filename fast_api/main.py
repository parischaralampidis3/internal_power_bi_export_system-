import os
import sys

# Add project root to PYTHONPATH
sys.path.insert(0, r"C:\Users\paris\Documents\internal_power_bi_export_system\power_bi_export_system")

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "power_bi_export_system.settings")

# Initialize Django
import django
django.setup()

# Now import FastAPI and routers
from fastapi import FastAPI
from fast_api.routers import run
from fast_api.routers.reports import router as reports_router
from fast_api.routers.pages import router as pages_router
from fast_api.routers.filters import router as filters_router
from fast_api.routers.export import router as export_router

# Create FastAPI app
app = FastAPI(title="Reports API", version="1.0.0")

app.include_router(reports_router, prefix="/api")
app.include_router(pages_router, prefix="/api")
app.include_router(filters_router, prefix="/api")  
app.include_router(export_router, prefix="/api") 
app.include_router(run.router, prefix="/api/export")

@app.get("/")
def read_root():
    return {"message": "Hello World"}
