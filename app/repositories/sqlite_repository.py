import sqlite3

from app.domain.models import Attempt, Feedback


class SQLiteRepository:
    def __init__(self, database_path: str):
        self.database_path = database_path
        self.create_tables()
        self.seed_problems()

    def connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def create_tables(self):
        with self.connect() as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS problems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    requirements TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    problem_id INTEGER NOT NULL,
                    class_names TEXT NOT NULL,
                    responsibilities TEXT NOT NULL,
                    relationships TEXT NOT NULL,
                    decisions TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    attempt_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    title TEXT NOT NULL,
                    explanation TEXT NOT NULL,
                    severity TEXT NOT NULL
                );
            """)

    def seed_problems(self):
        with self.connect() as connection:
            count = connection.execute(
                "SELECT COUNT(*) FROM problems"
            ).fetchone()[0]

            if count == 0:
                connection.executemany(
                    """
                    INSERT INTO problems(title, description, requirements)
                    VALUES (?, ?, ?)
                    """,
                    [
                        (
                            "Parking Lot",
                            "Design a parking lot system for vehicle entry, parking, and exit.",
                            "Support different vehicle types, parking spots, ticket creation, and fee calculation."
                        ),
                        (
                            "Vending Machine",
                            "Design a vending machine that sells products and handles payments.",
                            "Support product selection, payment, inventory, refunds, and out-of-stock handling."
                        )
                    ]
                )

    def get_problems(self):
        with self.connect() as connection:
            return connection.execute(
                "SELECT * FROM problems ORDER BY id"
            ).fetchall()

    def get_problem(self, problem_id: int):
        with self.connect() as connection:
            return connection.execute(
                "SELECT * FROM problems WHERE id = ?",
                (problem_id,)
            ).fetchone()

    def save_attempt(self, attempt: Attempt) -> int:
        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO attempts(
                    problem_id,
                    class_names,
                    responsibilities,
                    relationships,
                    decisions
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    attempt.problem_id,
                    attempt.class_names,
                    attempt.responsibilities,
                    attempt.relationships,
                    attempt.decisions
                )
            )

            return cursor.lastrowid

    def save_feedback(self, attempt_id: int, feedback: list[Feedback]):
        with self.connect() as connection:
            connection.executemany(
                """
                INSERT INTO feedback(
                    attempt_id,
                    category,
                    title,
                    explanation,
                    severity
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (
                        item_attempt_id,
                        item.category,
                        item.title,
                        item.explanation,
                        item.severity
                    )
                    for item_attempt_id in [attempt_id]
                    for item in feedback
                ]
            )

    def get_attempt_with_feedback(self, attempt_id: int):
        with self.connect() as connection:
            attempt = connection.execute(
                """
                SELECT attempts.*, problems.title
                FROM attempts
                JOIN problems ON problems.id = attempts.problem_id
                WHERE attempts.id = ?
                """,
                (attempt_id,)
            ).fetchone()

            if attempt is None:
                return None

            feedback = connection.execute(
                """
                SELECT *
                FROM feedback
                WHERE attempt_id = ?
                ORDER BY id
                """,
                (attempt_id,)
            ).fetchall()

            return {
                "attempt": attempt,
                "feedback": feedback
            }

    def get_attempts(self):
        with self.connect() as connection:
            return connection.execute(
                """
                SELECT attempts.id, problems.title, attempts.created_at
                FROM attempts
                JOIN problems ON problems.id = attempts.problem_id
                ORDER BY attempts.id DESC
                """
            ).fetchall()
