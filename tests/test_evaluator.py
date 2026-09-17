from app.domain.evaluator import RuleBasedEvaluator
from app.domain.models import Attempt


def make_attempt(
    class_names="",
    responsibilities="",
    relationships="",
    decisions=""
):
    return Attempt(
        problem_id=1,
        class_names=class_names,
        responsibilities=responsibilities,
        relationships=relationships,
        decisions=decisions
    )


def test_short_submission_creates_improvement_feedback():
    evaluator = RuleBasedEvaluator()
    feedback = evaluator.evaluate(make_attempt())

    assert len(feedback) == 4
    assert all(item.severity == "improvement" for item in feedback)


def test_detailed_submission_creates_positive_feedback():
    evaluator = RuleBasedEvaluator()
    feedback = evaluator.evaluate(
        make_attempt(
            class_names="ParkingLot, ParkingSpot, Vehicle",
            responsibilities="Each class has a clear and focused responsibility.",
            relationships="ParkingLot uses ParkingSpot and Vehicle through defined relationships.",
            decisions="Composition was selected to keep ownership clear and support change."
        )
    )

    assert len(feedback) == 4
    assert all(item.severity == "positive" for item in feedback)


def test_partial_submission_has_mixed_feedback():
    evaluator = RuleBasedEvaluator()
    feedback = evaluator.evaluate(
        make_attempt(
            class_names="Vehicle and ParkingLot",
            responsibilities="Each class owns a specific business behavior.",
            relationships="",
            decisions=""
        )
    )

    assert feedback[0].severity == "positive"
    assert feedback[1].severity == "positive"
    assert feedback[2].severity == "improvement"
    assert feedback[3].severity == "improvement"
