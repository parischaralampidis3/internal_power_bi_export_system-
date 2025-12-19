<<<<<<< HEAD
from fast_api import FastAPI
from routers import router as reports_router
=======
from fastapi import FastAPI
from routers.routes import router as reports_router

>>>>>>> fast_api
app = FastAPI()
app.include_router(reports_router, prefix="/api")

@app.get("/")
def read_root():
<<<<<<< HEAD
    return {"Hello": "World"}
=======
    return {"Hello": "World"}
>>>>>>> fast_api
