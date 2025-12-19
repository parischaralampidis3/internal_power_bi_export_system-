from fast_api import FastAPI
from routers import router as reports_router
app = FastAPI()
app.include_router(reports_router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}