from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from engine import InternetEraEngine
import os

app = FastAPI(title="Internet Era")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

engine = InternetEraEngine(os.environ.get("OPENROUTER_API_KEY"))

class QuizResponse(BaseModel):
    answers: list[int]
    name: str = ""

@app.get("/")
async def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.post("/api/analyze")
async def analyze(data: QuizResponse):
    if not data.answers or len(data.answers) != 8:
        raise HTTPException(400, "Need exactly 8 answers")
    try:
        result = engine.analyze(data.answers)
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
