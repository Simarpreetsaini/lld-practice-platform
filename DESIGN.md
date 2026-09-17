# Design Note

## Scope

The application is a small monolithic web application for practicing Low-Level Design. It supports problem browsing, text submissions, deterministic feedback, persistence, and attempt history.

## Architecture

```text
Browser
   |
   v
FastAPI routes
   |
   +--> Jinja2 templates
   |
   +--> RuleBasedEvaluator
   |
   +--> SQLiteRepository
           |
           v
        SQLite
```

## Main components

### FastAPI application

The application routes receive requests, validate the selected problem, coordinate submission processing, and select the template to render.

### Attempt

Represents a learner's submission for a problem. It contains classes, responsibilities, relationships, and design decisions.

### Feedback

Represents one evaluation result with a category, title, explanation, and severity.

### Evaluator

Defines the contract for evaluation implementations.

### RuleBasedEvaluator

Provides deterministic checks for whether the learner has supplied content in each design section.

### SQLiteRepository

Owns database setup, problem seeding, attempt persistence, feedback persistence, and history queries.

## Request flow

1. The learner opens a problem.
2. The learner submits the four design sections.
3. The route creates an `Attempt` object.
4. The repository saves the attempt.
5. The evaluator generates four feedback items.
6. The repository saves the feedback.
7. The user is redirected to the feedback page.

## Evaluation approach

The first version intentionally uses simple rules. This makes feedback predictable, easy to test, and easy to explain during an assignment demo.

The checks identify missing or short sections. They do not verify whether a class diagram is semantically correct, whether responsibilities are perfectly assigned, or whether the design is production-ready.

## Extensibility

A future evaluator can implement the same contract:

```python
class LlmEvaluator(Evaluator):
    def evaluate(self, attempt):
        ...
```

The route can continue to depend on the evaluator interface rather than a specific evaluation algorithm.

## Trade-offs

SQLite reduces setup effort but is not intended for a large multi-user deployment. Server-rendered templates reduce frontend complexity but provide less interactivity than a separate frontend. Synchronous evaluation keeps the MVP simple but would need a background job for slower external evaluation.
