from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from app.routers import analyze

app = FastAPI(title="Scrutin — Job Scam Detector")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(analyze.router)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
