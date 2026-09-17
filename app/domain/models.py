from dataclasses import dataclass


@dataclass
class Attempt:
    problem_id: int
    class_names: str
    responsibilities: str
    relationships: str
    decisions: str


@dataclass
class Feedback:
    category: str
    title: str
    explanation: str
    severity: str
