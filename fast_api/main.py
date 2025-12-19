from fastapi import FastAPI
from routers.routes import router as reports_router

app = FastAPI()
app.include_router(reports_router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}
