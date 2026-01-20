"""Progress tracking using SQLite."""

import sqlite3
from datetime import datetime
from pathlib import Path

from exrun.models import Exercise, ExerciseStatus, TestResult


class ProgressDB:
    """SQLite-based progress tracking."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        """Initialize database schema."""
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                order_num INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                attempts INTEGER DEFAULT 0,
                first_passed_at TIMESTAMP,
                last_attempt_at TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY,
                exercise_id INTEGER REFERENCES exercises(id),
                passed BOOLEAN NOT NULL,
                output TEXT,
                duration_ms INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS hints_shown (
                exercise_id INTEGER REFERENCES exercises(id),
                hint_index INTEGER,
                shown_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (exercise_id, hint_index)
            );
        """)
        self.conn.commit()

    def ensure_exercise(self, exercise: Exercise) -> int:
        """Ensure exercise exists in DB, return its ID."""
        cursor = self.conn.execute(
            "SELECT id FROM exercises WHERE name = ?", (exercise.name,)
        )
        row = cursor.fetchone()
        if row:
            return row["id"]

        cursor = self.conn.execute(
            "INSERT INTO exercises (name, order_num) VALUES (?, ?)",
            (exercise.name, exercise.order),
        )
        self.conn.commit()
        return cursor.lastrowid  # type: ignore[return-value]

    def get_status(self, exercise: Exercise) -> ExerciseStatus:
        """Get the status of an exercise."""
        cursor = self.conn.execute(
            "SELECT status FROM exercises WHERE name = ?", (exercise.name,)
        )
        row = cursor.fetchone()
        if not row:
            return ExerciseStatus.PENDING
        return ExerciseStatus(row["status"])

    def get_attempts(self, exercise: Exercise) -> int:
        """Get the number of attempts for an exercise."""
        cursor = self.conn.execute(
            "SELECT attempts FROM exercises WHERE name = ?", (exercise.name,)
        )
        row = cursor.fetchone()
        return row["attempts"] if row else 0

    def record_attempt(self, exercise: Exercise, result: TestResult) -> None:
        """Record an attempt for an exercise."""
        exercise_id = self.ensure_exercise(exercise)
        now = datetime.now().isoformat()

        self.conn.execute(
            """
            UPDATE exercises 
            SET attempts = attempts + 1, last_attempt_at = ?
            WHERE id = ?
            """,
            (now, exercise_id),
        )

        if result.passed:
            self.conn.execute(
                """
                UPDATE exercises 
                SET status = 'passed', first_passed_at = COALESCE(first_passed_at, ?)
                WHERE id = ?
                """,
                (now, exercise_id),
            )

        self.conn.execute(
            """
            INSERT INTO attempts (exercise_id, passed, output, duration_ms)
            VALUES (?, ?, ?, ?)
            """,
            (exercise_id, result.passed, result.output, result.duration_ms),
        )
        self.conn.commit()

    def mark_skipped(self, exercise: Exercise) -> None:
        """Mark an exercise as skipped."""
        exercise_id = self.ensure_exercise(exercise)
        self.conn.execute(
            "UPDATE exercises SET status = 'skipped' WHERE id = ?",
            (exercise_id,),
        )
        self.conn.commit()

    def get_hints_shown_count(self, exercise: Exercise) -> int:
        """Get how many hints have been shown for an exercise."""
        cursor = self.conn.execute(
            """
            SELECT COUNT(*) as count FROM hints_shown h
            JOIN exercises e ON h.exercise_id = e.id
            WHERE e.name = ?
            """,
            (exercise.name,),
        )
        return cursor.fetchone()["count"]

    def record_hint_shown(self, exercise: Exercise, hint_index: int) -> None:
        """Record that a hint was shown."""
        exercise_id = self.ensure_exercise(exercise)
        self.conn.execute(
            """
            INSERT OR IGNORE INTO hints_shown (exercise_id, hint_index)
            VALUES (?, ?)
            """,
            (exercise_id, hint_index),
        )
        self.conn.commit()

    def reset_all(self) -> None:
        """Reset all progress."""
        self.conn.executescript("""
            DELETE FROM hints_shown;
            DELETE FROM attempts;
            DELETE FROM exercises;
        """)
        self.conn.commit()

    def reset_exercise(self, exercise: Exercise) -> None:
        """Reset progress for a specific exercise."""
        cursor = self.conn.execute(
            "SELECT id FROM exercises WHERE name = ?", (exercise.name,)
        )
        row = cursor.fetchone()
        if not row:
            return

        exercise_id = row["id"]
        self.conn.execute("DELETE FROM hints_shown WHERE exercise_id = ?", (exercise_id,))
        self.conn.execute("DELETE FROM attempts WHERE exercise_id = ?", (exercise_id,))
        self.conn.execute(
            """
            UPDATE exercises 
            SET status = 'pending', attempts = 0, first_passed_at = NULL, last_attempt_at = NULL
            WHERE id = ?
            """,
            (exercise_id,),
        )
        self.conn.commit()

    def get_all_statuses(self) -> dict[str, ExerciseStatus]:
        """Get status for all exercises."""
        cursor = self.conn.execute("SELECT name, status FROM exercises")
        return {row["name"]: ExerciseStatus(row["status"]) for row in cursor}

    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()
