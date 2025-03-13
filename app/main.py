from fastapi import FastAPI
from app.api import routes

app = FastAPI(title="Crypto Agent")

app.include_router(routes.router)

@app.get("/")
def health_check():
    return {"status": "Crypto Agent is running!"}
