from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.domain.evaluator import RuleBasedEvaluator
from app.domain.models import Attempt
from app.repositories.sqlite_repository import SQLiteRepository

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="LLD Practice Platform")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")
repository = SQLiteRepository("lld_practice.db")
evaluator = RuleBasedEvaluator()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    problems = repository.get_problems()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "problems": problems}
    )


@app.get("/problems/{problem_id}", response_class=HTMLResponse)
def problem_detail(request: Request, problem_id: int):
    problem = repository.get_problem(problem_id)

    if problem is None:
        return HTMLResponse("Problem not found", status_code=404)

    return templates.TemplateResponse(
        "problem.html",
        {"request": request, "problem": problem}
    )


@app.post("/problems/{problem_id}/submit")
def submit_attempt(
    problem_id: int,
    class_names: str = Form(...),
    responsibilities: str = Form(...),
    relationships: str = Form(...),
    decisions: str = Form(...)
):
    problem = repository.get_problem(problem_id)

    if problem is None:
        return HTMLResponse("Problem not found", status_code=404)

    attempt = Attempt(
        problem_id=problem_id,
        class_names=class_names,
        responsibilities=responsibilities,
        relationships=relationships,
        decisions=decisions
    )

    attempt_id = repository.save_attempt(attempt)
    feedback = evaluator.evaluate(attempt)
    repository.save_feedback(attempt_id, feedback)

    return RedirectResponse(
        f"/attempts/{attempt_id}",
        status_code=303
    )


@app.get("/attempts/{attempt_id}", response_class=HTMLResponse)
def attempt_detail(request: Request, attempt_id: int):
    result = repository.get_attempt_with_feedback(attempt_id)

    if result is None:
        return HTMLResponse("Attempt not found", status_code=404)

    return templates.TemplateResponse(
        "attempt.html",
        {"request": request, "result": result}
    )


@app.get("/history", response_class=HTMLResponse)
def history(request: Request):
    attempts = repository.get_attempts()

    return templates.TemplateResponse(
        "history.html",
        {"request": request, "attempts": attempts}
    )
