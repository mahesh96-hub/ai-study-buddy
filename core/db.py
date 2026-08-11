import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/study_buddy.db")


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def init_db():
    connection = get_connection()

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS materials (
            material_id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            upload_date TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS questions (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            question_type TEXT NOT NULL,
            question_text TEXT NOT NULL,
            options_json TEXT,
            correct_answer TEXT NOT NULL,
            last_attempt TEXT,
            last_score REAL,
            attempt_count INTEGER DEFAULT 0,
            next_review_date TEXT,
            FOREIGN KEY (material_id) REFERENCES materials(material_id)
        );

        CREATE TABLE IF NOT EXISTS attempts (
            attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            user_answer TEXT,
            score REAL NOT NULL,
            feedback TEXT,
            answered_at TEXT NOT NULL,
            FOREIGN KEY (question_id) REFERENCES questions(question_id)
        );
        """
    )

    connection.commit()
    connection.close()