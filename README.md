# LLD Practice Platform

A small web application for practicing Low-Level Design (LLD). Learners choose a design problem, submit a text-based solution, receive explainable rule-based feedback, and review previous attempts.

## Project goal

The project focuses on a simple, understandable architecture that can be implemented and demonstrated within a short engineering assignment.

## Features

- Browse multiple LLD practice problems
- Submit classes and interfaces
- Describe class responsibilities
- Describe relationships and dependencies
- Explain design decisions and trade-offs
- Store attempts and feedback in SQLite
- View previous attempts through history
- Run automated evaluator tests
- Use a replaceable evaluator interface for future AI-based evaluation

## Technology stack

- Python 3.11+
- FastAPI
- Uvicorn
- Jinja2 templates
- SQLite
- Pytest

## Project structure

```text
lld-practice-platform/
├── app/
│   ├── domain/
│   │   ├── evaluator.py
│   │   └── models.py
│   ├── repositories/
│   │   └── sqlite_repository.py
│   ├── templates/
│   ├── static/
│   └── main.py
├── tests/
│   └── test_evaluator.py
├── AI_USAGE.md
├── DESIGN.md
├── RESEARCH.md
├── README.md
├── requirements.txt
└── .gitignore
```

## Setup on Windows

Open PowerShell in the project root.

### 1. Create a virtual environment

```powershell
python -m venv .venv
```

### 2. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run the following command in a PowerShell window opened with the required permissions:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate the environment again.

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run tests

```powershell
python -m pytest
```

### 5. Start the application

```powershell
uvicorn app.main:app --reload
```

Open the application at:

```text
http://127.0.0.1:8000/
```

Keep the server terminal running while using the website. Use a second terminal for tests or other commands.

## Main user flow

1. Open the homepage.
2. Select a problem.
3. Fill in the four design sections.
4. Submit the solution.
5. Read the generated feedback.
6. Open the history page to review previous attempts.

## Evaluation approach

The current evaluator is deterministic and rule-based. It checks whether each submission section contains enough information to encourage further design reasoning.

The evaluator does not prove that a design is correct. It does not replace a human design review, UML review, code review, or production architecture assessment.

## Design decisions

- FastAPI and server-rendered Jinja2 templates keep the frontend simple.
- SQLite avoids external database setup for the MVP.
- Repository code is separated from domain evaluation logic.
- The `Evaluator` abstraction allows another evaluation implementation to be added later.
- Text input was selected instead of building a diagram editor to keep the initial scope achievable.

## Known limitations

- No authentication or user accounts
- Local SQLite database
- Text-only design submissions
- Rule-based feedback rather than deep semantic evaluation
- No diagram editor or automatic UML generation
- Synchronous evaluation

## Future improvements

- Add a rubric-based score and category summary
- Add more problem types
- Add stronger checks for SOLID principles and design patterns
- Add optional LLM evaluation behind a feature flag
- Add user accounts and per-user history
- Add diagram upload or UML support
- Add API and repository integration tests
- Add deployment configuration

## Assignment demo checklist

- [ ] Install dependencies successfully
- [ ] Run all tests successfully
- [ ] Start the FastAPI server
- [ ] Open the homepage
- [ ] Submit a Parking Lot design
- [ ] Submit a Vending Machine design
- [ ] Open both feedback pages
- [ ] Verify attempt history
- [ ] Explain the architecture and trade-offs
- [ ] Explain the evaluator limitations

## Live Demo

https://lld-practice-platform-1-byjy.onrender.com/
