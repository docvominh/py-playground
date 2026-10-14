from fastapi import FastAPI

from app.api.movies import router as movies_router

app = FastAPI(title="My API")
app.include_router(movies_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
