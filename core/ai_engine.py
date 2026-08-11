import os

from dotenv import load_dotenv
from google import genai

from core.schemas import QuestionList, Evaluation


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_questions(
    study_text: str,
    number_of_questions: int = 5
) -> QuestionList:

    prompt = f"""
You are an exam question generator.

Read the study material below and generate {number_of_questions} quiz questions
covering its important concepts.

Mix the question types:
- MCQ
- TrueFalse
- ShortAnswer

Rules:
- MCQ must have exactly 4 options.
- TrueFalse must have exactly ["True", "False"] as options.
- ShortAnswer must have options set to null.
- The correct_answer must exactly match one of the options for MCQ and TrueFalse.
- Keep questions clear and suitable for a college student.
- Generate questions only from the provided study material.

Study material:
\"\"\"
{study_text}
\"\"\"
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": QuestionList,
        },
    )

    return QuestionList.model_validate_json(response.text)


def evaluate_answer(
    question_text: str,
    correct_answer: str,
    student_answer: str
) -> Evaluation:

    prompt = f"""
You are grading a student's short answer.

Question:
{question_text}

Correct answer:
{correct_answer}

Student answer:
{student_answer}

Judge the student's answer for correctness and completeness.

Use these scoring rules:
- Correct = 1.0
- Partially Correct = 0.5
- Wrong = 0.0

Return a short feedback sentence explaining why the answer received
that score.

Return only the structured evaluation.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": Evaluation,
        },
    )

    return Evaluation.model_validate_json(response.text)