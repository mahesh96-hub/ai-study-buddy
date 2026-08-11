import sqlite3
import json
from pathlib import Path
from datetime import datetime


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


def add_material(filename):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO materials (filename, upload_date)
        VALUES (?, ?)
        """,
        (filename, datetime.now().isoformat())
    )

    material_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return material_id


def add_question(
    material_id,
    topic,
    question_type,
    question_text,
    options,
    correct_answer
):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO questions (
            material_id,
            topic,
            question_type,
            question_text,
            options_json,
            correct_answer
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            material_id,
            topic,
            question_type,
            question_text,
            json.dumps(options) if options else None,
            correct_answer
        )
    )

    question_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return question_id


def add_attempt(
    question_id,
    user_answer,
    score,
    feedback
):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO attempts (
            question_id,
            user_answer,
            score,
            feedback,
            answered_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            question_id,
            user_answer,
            score,
            feedback,
            datetime.now().isoformat()
        )
    )

    attempt_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return attempt_id