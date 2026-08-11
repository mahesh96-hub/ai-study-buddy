📚 AI Study Buddy

An AI-powered personalized learning platform that converts study materials into adaptive quizzes, evaluates student answers, schedules reviews using spaced repetition, and provides personalized learning analytics.

📌 Project Overview

AI Study Buddy is an intelligent learning assistant designed to help students study more effectively from their own learning materials.

Instead of manually creating questions from lecture notes, textbooks, syllabi, question banks, and other study materials, students can upload PDF documents and allow the system to automatically analyze the content and generate quiz questions.

The system combines:

Artificial Intelligence

Natural Language Processing

Automated Question Generation

AI-based Answer Evaluation

Spaced Repetition

Personalized Learning Analytics

User Authentication

Multi-material Learning

Each authenticated student has an independent learning environment where their study materials, questions, quiz attempts, review schedules, and dashboard statistics are isolated from other users.

🎯 Problem Statement

Students commonly study using large amounts of lecture notes, textbooks, PDFs, syllabi, question banks, and other learning materials.

However, several problems exist with traditional study methods:

Students spend significant time manually preparing questions.

It is difficult to identify which topics need more revision.

Students often review all topics equally instead of focusing on weak areas.

Traditional quizzes provide limited personalized feedback.

Students may forget previously studied concepts without regular revision.

There is usually no automated mechanism for scheduling future reviews.

Learning progress is often tracked manually.

Different study materials require different amounts of practice.

The goal of AI Study Buddy is to solve these problems by automatically converting a student's study material into an adaptive and personalized learning experience.


💡 Proposed Solution


AI Study Buddy provides an automated learning pipeline:

Student
   │
   ▼
Google Authentication
   │
   ▼
Upload Study Material
   │
   ▼
PDF Analysis
   │
   ├── Page Count
   │
   └── Text Extraction
   │
   ▼
Adaptive Question Generation
   │
   ▼
AI Generated Questions
   │
   ▼
Interactive Quiz
   │
   ▼
Answer Evaluation
   │
   ├── Objective Evaluation
   │
   └── AI Short-Answer Evaluation
   │
   ▼
Score + Feedback
   │
   ▼
Spaced Repetition Scheduler
   │
   ▼
Future Review
   │
   ▼
Personalized Dashboard



🎯 Objectives

The main objectives of the project are:

Automatically generate quiz questions from study materials.

Support multiple PDF study materials.

Generate questions according to the size of each PDF.

Keep every uploaded material independent.

Provide user-specific learning environments.

Evaluate student answers automatically.

Provide meaningful feedback.

Schedule future reviews based on performance.

Identify mastered and weak questions.

Provide personalized learning analytics.

Reduce manual quiz preparation.

Improve long-term knowledge retention.


🚀 Key Features


🔐 1. Google Authentication

Students authenticate using Google.

The system assigns a unique identity to each authenticated user.

Google Account
      │
      ▼
Authenticated User
      │
      ▼
Unique User ID
      │
      ├── Materials
      ├── Questions
      ├── Attempts
      ├── Reviews
      └── Dashboard


📄 2. Multiple Study Material Upload


Students can upload multiple PDF files at the same time.

Example:

Cyber Security Notes.pdf
AI Unit 1.pdf
Cloud Computing Notes.pdf
Question Bank.pdf

Each PDF is processed independently.

Each uploaded PDF receives its own:

Material ID

Extracted content

Question set

Quiz

Review history

Learning progress


📑 3. Adaptive Question Generation


The number of generated questions depends on the number of pages in each PDF.

PDF Page Count

Generated Questions

1–9 pages

5 questions

10–20 pages

15 questions

21–50 pages

25 questions

51+ pages

35 questions

Example

Cyber Security.pdf
18 pages
→ 15 questions

Machine Learning.pdf
35 pages
→ 25 questions

Cloud Computing.pdf
70 pages
→ 35 questions


📚 4. Independent Material Processing


Multiple PDFs are never merged into a single question set.

Student
   │
   ├── PDF A
   │     └── 18 pages
   │           └── 15 questions
   │
   ├── PDF B
   │     └── 35 pages
   │           └── 25 questions
   │
   └── PDF C
         └── 70 pages
               └── 35 questions

Each material maintains its own questions.


🧠 5. AI Question Generation


The extracted PDF text is sent to the AI engine.

The AI engine generates structured questions containing:

Topic

Question type

Question text

Options

Correct answer

Supported question types include:

Multiple Choice Question

Which of the following is a security principle?

A. Confidentiality
B. Compression
C. Compilation
D. Rendering

True/False

AES is a symmetric encryption algorithm.

True
False

Short Answer

What is the primary purpose of a firewall?


📝 6. Interactive Quiz


Students can select a study material from their uploaded materials.

📚 Select study material

[ Cyber Security Notes.pdf ▼ ]

The system then displays only questions belonging to that material.

The Quiz page supports:

MCQs

True/False questions

Short-answer questions

Students can submit the quiz and receive an immediate result.


🤖 7. AI-Based Short Answer Evaluation


Objective questions such as MCQs and True/False questions are evaluated directly.

Short-answer questions are evaluated using the AI evaluation engine.

The evaluation provides:

Score

Correctness status

Feedback

Example:

Status: Correct

Score: 1.0

Feedback:
The student correctly explained the main purpose
of cybersecurity by identifying the protection of
systems and data from unauthorized access.

This allows the system to evaluate answers based on meaning rather than exact text matching.


📊 8. Quiz Scoring


Every question receives a score.

The current scoring model supports:

1.0 → Correct
0.5 → Partially Correct
0.0 → Incorrect

The final quiz percentage is calculated from the scores of all questions.


🔄 9. Spaced Repetition


AI Study Buddy uses performance-based scheduling to determine when a question should appear again.

Student answers
      │
      ▼
Evaluate performance
      │
      ├── Correct
      ├── Partially Correct
      └── Incorrect
      │
      ▼
Calculate next review date

Example:

Correct
    ↓
Review after a longer interval

Partially Correct
    ↓
Review sooner

Incorrect
    ↓
Review again quickly


📅 10. Review System


The Review page displays questions that are currently due for review.

The system:

Evaluates the answers.

Records the attempt.

Calculates the new score.

Calculates the next review date.

Updates the question's review schedule.


📈 11. Personalized Dashboard


The Dashboard provides an overview of the student's learning progress.

It includes:

Total study materials

Total questions

Total attempts

Average score

Questions due today

Questions mastered

Questions needing improvement

Overall accuracy

Upcoming reviews


👤 12. Multi-User Data Isolation


Every student has an independent learning environment.

Student A

Student A
   │
   ├── Notes.pdf
   ├── AI.pdf
   ├── Cyber Security.pdf
   │
   ├── Questions
   ├── Attempts
   ├── Reviews
   └── Dashboard

Student B

Student B
   │
   ├── Cloud.pdf
   ├── Networking.pdf
   │
   ├── Questions
   ├── Attempts
   ├── Reviews
   └── Dashboard

Student A cannot access Student B's study materials or learning statistics.

🏗️ System Architecture

                         ┌──────────────────────┐
                         │      Student         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Google Login       │
                         │   OAuth / OIDC       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                              Unique User ID
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Study Material Page  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                           Upload PDF(s)
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    PDF Processor     │
                         │      PyMuPDF         │
                         └──────────┬───────────┘
                                    │
                       ┌────────────┴────────────┐
                       │                         │
                       ▼                         ▼
                  Page Count                Text Extraction
                       │                         │
                       ▼                         │
                Question Count                  │
                       │                         │
                       └────────────┬────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │      AI Engine       │
                         │     Gemini API       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         Generated Questions
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   SQLite Database    │
                         └──────────┬───────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
      │     Quiz     │      │    Review    │      │  Dashboard   │
      └──────┬───────┘      └──────┬───────┘      └──────┬───────┘
             │                     │                     │
             ▼                     ▼                     ▼
       Answer Check          Spaced Repetition       Analytics

🔄 Complete Application Workflow

Step 1 — User Authentication

Student opens application
        ↓
Google Login
        ↓
Authenticated

Step 2 — Upload Study Materials

Student selects PDF(s)
        ↓
PDF validation
        ↓
Page counting

Step 3 — Determine Question Count

Page Count
    │
    ├── 1–9       → 5
    ├── 10–20     → 15
    ├── 21–50     → 25
    └── 51+       → 35

Step 4 — Extract PDF Content

PDF
 ↓
PyMuPDF
 ↓
Extracted Text

Step 5 — Generate Questions

Extracted Text
      ↓
Gemini AI
      ↓
Structured Questions

Step 6 — Store Material and Questions

User ID
   │
   ▼
Material
   │
   ▼
Questions

Step 7 — Take Quiz

Select Material
      ↓
Load Questions
      ↓
Answer Questions
      ↓
Submit Quiz

Step 8 — Evaluate Answers

MCQ / TrueFalse
        ↓
Direct Evaluation

Short Answer
        ↓
Gemini Evaluation

Step 9 — Store Attempt

Each attempt records:

Question ID

Student answer

Score

Feedback

Answer timestamp

Step 10 — Schedule Review

Score
 ↓
Spaced Repetition Scheduler
 ↓
Next Review Date

Step 11 — Review Due Questions

Review Page
     ↓
Due Questions
     ↓
Student Answers
     ↓
Evaluation
     ↓
New Review Date

Step 12 — Dashboard

Materials
Questions
Attempts
Accuracy
Mastered Questions
Weak Questions
Upcoming Reviews

🗄️ Database Design

The application currently uses SQLite.

Main tables:

materials
questions
attempts

Materials Table

materials
├── material_id
├── user_id
├── filename
└── upload_date

Questions Table

questions
├── question_id
├── material_id
├── topic
├── question_type
├── question_text
├── options_json
├── correct_answer
├── last_attempt
├── last_score
├── attempt_count
└── next_review_date

Attempts Table

attempts
├── attempt_id
├── question_id
├── user_answer
├── score
├── feedback
└── answered_at

Database Relationship

User
 │
 │ user_id
 ▼
Materials
 │
 │ material_id
 ▼
Questions
 │
 │ question_id
 ▼
Attempts


🧩 Core Modules


core/auth.py

Handles:

Google authentication

Login state

User identity

Logout

core/db.py

Handles:

SQLite connection

Database initialization

Database migration

Materials

Questions

Attempts

Review updates

core/ai_engine.py

Handles:

AI question generation

Short-answer evaluation

AI feedback

core/pdf_processor.py

Handles:

PDF processing

Text extraction

core/scheduler.py

Handles:

Review scheduling

Next review date calculation

core/schemas.py

Defines structured data models used by the AI engine.


🖥️ Application Pages


📄 Study Material


Responsible for:

Uploading PDFs

Processing multiple PDFs

Counting pages

Extracting text

Generating questions

Storing materials


📝 Quiz


Responsible for:

Selecting study material

Displaying questions

Collecting answers

Evaluating answers

Calculating score

Saving attempts

Scheduling reviews


🔄 Review


Responsible for:

Finding due questions

Reviewing weak/old questions

Evaluating review answers

Updating review schedules


📊 Dashboard


Responsible for:

Progress statistics

Accuracy

Materials

Attempts

Mastered questions

Weak questions

Upcoming reviews


🛠️ Technology Stack


Category

Technology

Programming Language

Python

Frontend

Streamlit

AI Model

Google Gemini

Authentication

Google OAuth / OpenID Connect

PDF Processing

PyMuPDF

Database

SQLite

Data Validation

Pydantic

Environment Configuration

python-dotenv

Version Control

Git

Repository

GitHub


📁 Project Structure


ai-study-buddy/
│
├── app.py
├── README.md
├── LICENSE
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
│
├── .streamlit/
│   └── secrets.toml
│
├── core/
│   ├── __init__.py
│   ├── ai_engine.py
│   ├── auth.py
│   ├── db.py
│   ├── pdf_processor.py
│   ├── scheduler.py
│   └── schemas.py
│
├── pages/
│   ├── 1_Home.py
│   ├── 2_Quiz.py
│   ├── 3_Review.py
│   └── 4_Dashboard.py
│
└── data/
    └── study_buddy.db

⚙️ Installation

1. Clone the Repository

git clone https://github.com/mahesh96-hub/ai-study-buddy.git
cd ai-study-buddy

2. Create Virtual Environment

python3 -m venv venv

3. Activate Virtual Environment

macOS / Linux

source venv/bin/activate

Windows

venv\Scripts\activate

4. Install Dependencies

pip install -r requirements.txt

🔑 Environment Variables

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key

Never commit .env to GitHub.

🔐 Google Authentication Setup

Create:

.streamlit/secrets.toml

Add:

[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "YOUR_RANDOM_SECRET"
client_id = "YOUR_GOOGLE_CLIENT_ID"
client_secret = "YOUR_GOOGLE_CLIENT_SECRET"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"

Replace the placeholder values with your actual credentials.

For production deployment, update the redirect URI to the deployed application's OAuth callback URL.

Never commit:

.streamlit/secrets.toml

to GitHub.

▶️ Run the Application

streamlit run app.py

The application will open in your browser.

🧪 Testing

Authentication Test

Google Login
     ↓
Authenticated
     ↓
User-specific application

PDF Test

Upload PDF
     ↓
Page Count
     ↓
Question Count
     ↓
Question Generation

Quiz Test

Select Material
     ↓
Answer Questions
     ↓
Submit
     ↓
Score + Feedback

Review Test

Due Question
     ↓
Review
     ↓
New Score
     ↓
New Review Date

User Isolation Test

Student A Login
     ↓
Upload Material
     ↓
Logout

Student B Login
     ↓
Student A material should NOT appear

🔒 Security Considerations

Authentication

Google authentication is used instead of storing user passwords directly in the application.

User Isolation

Database queries use the authenticated user's identifier when accessing materials and related data.

Secrets Protection

Sensitive credentials are stored outside the source code.

Examples:

.env
.streamlit/secrets.toml

These files should not be committed to GitHub.

Database Relationships

Questions are connected to materials, and attempts are connected to questions.

User
 ↓
Material
 ↓
Question
 ↓
Attempt

📈 Example Learning Scenario

A student studying Cyber Security uploads:

Cyber Security Unit 1.pdf

The PDF contains 18 pages.

The system determines:

18 pages
   ↓
15 questions

Gemini generates questions.

The student takes the quiz.

The system evaluates the answers, stores the attempt, calculates the score, and schedules future reviews.

Later:

Review Due
    ↓
Student reviews questions
    ↓
Performance updated
    ↓
Next review date recalculated

The Dashboard updates automatically.

🌟 Why AI Study Buddy?

Traditional learning systems often focus primarily on content delivery.

AI Study Buddy focuses on the complete learning cycle:

Study
 ↓
Practice
 ↓
Evaluate
 ↓
Review
 ↓
Track
 ↓
Improve

The system makes the learning process personalized rather than treating every student and every topic identically.

🔮 Future Scope

Potential future improvements include:

DOCX support

PPTX support

TXT support

Image/OCR-based study materials

Scanned PDF support

Automatic topic extraction

Difficulty-level selection

Question customization

Flashcards

Learning analytics

Performance graphs

Subject-wise progress

Weekly study trends

Learning streaks

Weak-topic detection

Personalized difficulty

Cloud database support

Mobile-friendly interface

Production deployment

📌 Current Project Status

✅ Google Authentication
✅ Multi-user data isolation
✅ Multiple PDF upload
✅ PDF page counting
✅ Adaptive question generation
✅ Independent material processing
✅ AI question generation
✅ MCQ evaluation
✅ True/False evaluation
✅ AI short-answer evaluation
✅ Quiz scoring
✅ Attempt tracking
✅ Spaced repetition
✅ Review system
✅ Personalized dashboard
✅ Upcoming review tracking

🧭 Complete Feature Flow

                    START
                      │
                      ▼
               Google Login
                      │
                      ▼
                Authenticated?
                 /          \
               No            Yes
               │              │
               ▼              ▼
             Login       Study Material
                              │
                              ▼
                         Upload PDF(s)
                              │
                              ▼
                         Count Pages
                              │
                              ▼
                   Determine Question Count
                              │
              ┌───────────────┼───────────────┐
              │               │               │
             5 Q             15 Q             25 Q
              │               │               │
           1–9 pages      10–20 pages      21–50 pages
                                              │
                                              ▼
                                         35 Questions
                                           51+ pages
                              │
                              ▼
                       Extract PDF Text
                              │
                              ▼
                         Gemini AI
                              │
                              ▼
                    Generate Questions
                              │
                              ▼
                       Store in DB
                              │
                              ▼
                            Quiz
                              │
                              ▼
                       Answer Questions
                              │
                              ▼
                          Evaluate
                              │
                              ▼
                       Score + Feedback
                              │
                              ▼
                    Spaced Repetition
                              │
                              ▼
                         Review Due
                              │
                              ▼
                     Personalized Review
                              │
                              ▼
                         Dashboard
                              │
                              ▼
                             END

👨‍💻 Author

K Mahesh Reddy

B.Tech — Cyber Security

Interests:

Cyber Security

Artificial Intelligence

Machine Learning

Cloud Computing

AI-powered applications

📄 License

This project will be released under the license specified in the LICENSE file.

⭐ Acknowledgement

This project was developed as an academic and portfolio project to explore the integration of Artificial Intelligence, personalized learning, automated assessment, and spaced repetition into a single learning platform.