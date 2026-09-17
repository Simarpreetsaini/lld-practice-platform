# Research Note

## Learner problem

LLD learners can create a solution but may not know whether their classes have clear responsibilities, whether dependencies are appropriate, or whether their design can be changed easily.

A practice platform should ask learners to explain classes, responsibilities, relationships, and trade-offs. Feedback should explain how to improve instead of only giving a score.

## Existing approaches

Written interview questions provide flexibility but often lack structured feedback. Coding platforms can test executable behavior but may not fully evaluate object responsibilities. Diagramming tools help with visualization but do not always provide a complete practice and review loop.

## Product direction

The MVP supports this flow:

1. Select a problem.
2. Write a design.
3. Submit the attempt.
4. Receive structured feedback.
5. Review previous attempts.

The first version uses deterministic checks because they are transparent, inexpensive, and easy to test. An LLM evaluator can be added later through the evaluator abstraction.
