from pydantic import BaseModel
from typing import Literal


class Question(BaseModel):
    topic: str
    question_type: Literal["MCQ", "TrueFalse", "ShortAnswer"]
    question_text: str
    options: list[str] | None
    correct_answer: str


class QuestionList(BaseModel):
    questions: list[Question]