from app.domain.models import Attempt, Feedback


class Evaluator:
    def evaluate(self, attempt: Attempt) -> list[Feedback]:
        raise NotImplementedError


class RuleBasedEvaluator(Evaluator):
    def evaluate(self, attempt: Attempt) -> list[Feedback]:
        feedback = []

        feedback.append(self.check_classes(attempt))
        feedback.append(self.check_responsibilities(attempt))
        feedback.append(self.check_relationships(attempt))
        feedback.append(self.check_decisions(attempt))

        return feedback

    def check_classes(self, attempt: Attempt) -> Feedback:
        if len(attempt.class_names.strip()) < 10:
            return Feedback(
                category="Abstractions",
                title="Add more meaningful classes",
                explanation="List the main classes or interfaces involved in the problem.",
                severity="improvement"
            )

        return Feedback(
            category="Abstractions",
            title="Classes were provided",
            explanation="Check that each class has one clear responsibility.",
            severity="positive"
        )

    def check_responsibilities(self, attempt: Attempt) -> Feedback:
        if len(attempt.responsibilities.strip()) < 20:
            return Feedback(
                category="Responsibilities",
                title="Explain responsibilities in more detail",
                explanation="Describe what each class owns and which behavior it performs.",
                severity="improvement"
            )

        return Feedback(
            category="Responsibilities",
            title="Responsibilities were included",
            explanation="Review whether business logic is placed in the right class.",
            severity="positive"
        )

    def check_relationships(self, attempt: Attempt) -> Feedback:
        if len(attempt.relationships.strip()) < 20:
            return Feedback(
                category="Relationships",
                title="Describe class relationships",
                explanation="Explain how classes interact and where dependencies exist.",
                severity="improvement"
            )

        return Feedback(
            category="Relationships",
            title="Relationships were included",
            explanation="Check whether dependencies use abstractions where appropriate.",
            severity="positive"
        )

    def check_decisions(self, attempt: Attempt) -> Feedback:
        if len(attempt.decisions.strip()) < 20:
            return Feedback(
                category="Trade-offs",
                title="Explain a design trade-off",
                explanation="Describe why you selected your design and mention an alternative.",
                severity="improvement"
            )

        return Feedback(
            category="Trade-offs",
            title="Design decisions were included",
            explanation="Connect your design decisions to the problem requirements.",
            severity="positive"
        )
