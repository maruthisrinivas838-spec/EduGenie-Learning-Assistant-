from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from explanation_module import explain_topic
from qna import answer_question
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations

app = FastAPI(
    title="EduGenie Learning Assistant",
    version="1.0"
)

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Static Files
# -------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

# -------------------------
# Templates
# -------------------------
templates = Jinja2Templates(directory="templates")

# -------------------------
# Home Page
# -------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# ==========================================================
# Request Models
# ==========================================================

class QuestionRequest(BaseModel):
    question: str


class TopicRequest(BaseModel):
    topic: str


class SummaryRequest(BaseModel):
    text: str


class QuizRequest(BaseModel):
    text: str


# ==========================================================
# Question Answer
# ==========================================================

@app.post("/qna")
async def qna(data: QuestionRequest):

    answer = answer_question(data.question)

    return {
        "answer": answer
    }


# ==========================================================
# Explanation
# ==========================================================

@app.post("/explain")
async def explanation(data: TopicRequest):

    result = explain_topic(data.topic)

    return {
        "explanation": result
    }


# ==========================================================
# Summary
# ==========================================================

@app.post("/summary")
async def summary(data: SummaryRequest):

    result = summarize_text(data.text)

    return {
        "summary": result
    }


# ==========================================================
# Quiz
# ==========================================================

@app.post("/quiz")
async def quiz(data: QuizRequest):

    quiz = generate_quiz(data.text)

    return {
        "quiz": quiz
    }


# ==========================================================
# Learning Path
# ==========================================================

@app.post("/learning-path")
async def roadmap(data: TopicRequest):

    roadmap = get_learning_recommendations(data.topic)

    return {
        "learning_path": roadmap
    }