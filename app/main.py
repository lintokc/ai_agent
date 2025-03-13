from fastapi import FastAPI
from app.api import routes

app = FastAPI(title="AI Agent")

app.include_router(routes.router)

@app.get("/")
def health_check():
    return {"status": "AI Agent is running"}
