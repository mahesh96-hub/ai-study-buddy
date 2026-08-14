

# 📚 AI Study Buddy

**Turn any PDF into a personalized, adaptive learning experience.**

AI Study Buddy converts study materials into adaptive quizzes, evaluates answers with AI, schedules spaced-repetition reviews, and tracks progress — automatically.

[Overview](#-project-overview) • [Features](#-key-features) • [Architecture](#️-system-architecture) • [Installation](#️-installation) • [Tech Stack](#️-technology-stack) • [Roadmap](#-future-scope)

</div>

---

## 📌 Project Overview

Studying from lecture notes, textbooks, syllabi, and question banks usually means manually writing your own practice questions, tracking which topics need more work, and remembering when to revisit them. **AI Study Buddy automates the entire loop.**

Upload a PDF → the system extracts the content, generates an appropriately-sized quiz with AI, evaluates your answers (including free-text short answers by meaning, not exact wording), schedules the next review using spaced repetition, and rolls everything up into a personalized dashboard.

Every student gets a fully isolated learning environment — their materials, questions, attempts, and analytics never mix with anyone else's.

**Built with:** Natural Language Processing · Automated Question Generation · AI Answer Evaluation · Spaced Repetition · Personalized Analytics · Multi-user Authentication

---

## 🎯 Problem Statement

| Traditional Studying | The Gap |
|---|---|
| Manually writing practice questions | Time-consuming, easy to skip |
| Reviewing everything equally | No focus on actual weak spots |
| Quizzes with no real feedback | Can't tell *why* an answer was wrong |
| No structured revision schedule | Concepts fade without spaced review |
| Manual progress tracking | Hard to see improvement over time |

**AI Study Buddy's goal:** turn any uploaded study material into an adaptive, self-correcting learning pipeline — with zero manual question-writing.

---

## 💡 Proposed Solution — The Pipeline

```
Student → Google Auth → Upload Study Material → PDF Analysis
   → Adaptive Question Generation → Interactive Quiz
   → Answer Evaluation (Objective + AI Short-Answer)
   → Score + Feedback → Spaced Repetition Scheduler
   → Future Review → Personalized Dashboard
```

---

## 🚀 Key Features

### 🔐 Google Authentication
Every student signs in with Google and gets a unique ID that scopes all of their materials, questions, attempts, reviews, and dashboard data.

### 📄 Multiple, Independent Study Materials
Upload several PDFs at once — each is processed **independently**, with its own material ID, extracted content, question set, quiz, and review history. Materials are never merged.

### 📑 Adaptive Question Generation
Question count scales with document length, so a syllabus and a 70-page textbook chapter don't get the same treatment:

| PDF Length | Questions Generated |
|:---:|:---:|
| 1–9 pages | 5 |
| 10–20 pages | 15 |
| 21–50 pages | 25 |
| 51+ pages | 35 |

**Example:** `Machine Learning.pdf` (35 pages) → 25 questions · `Cloud Computing.pdf` (70 pages) → 35 questions

### 🧠 AI-Generated, Multi-Format Questions
Extracted text is sent to Gemini, which returns structured questions with topic, type, options, and correct answer — across three formats:
- **Multiple Choice** — 4 options, one correct
- **True / False**
- **Short Answer** — open-ended, evaluated by meaning

### 📝 Interactive Quiz
Pick a material, get a quiz built only from that material's questions, answer MCQs / True-False / short-answer items, and submit for an instant result.

### 🤖 AI-Based Short-Answer Evaluation
Objective questions are checked directly; short answers are evaluated by Gemini for *semantic* correctness, not string matching — returning a score, a correctness status, and written feedback.

> **Example**
> Status: `Correct` · Score: `1.0`
> Feedback: *"The student correctly explained the main purpose of cybersecurity by identifying the protection of systems and data from unauthorized access."*

### 📊 Scoring
Each question scores `1.0` (Correct) · `0.5` (Partially Correct) · `0.0` (Incorrect), rolled up into a final quiz percentage.

### 🔄 Spaced Repetition
Performance drives the next review date:

| Result | Next Review |
|---|---|
| ✅ Correct | Longer interval |
| ⚠️ Partially Correct | Sooner |
| ❌ Incorrect | Very soon |

### 📅 Review System
A dedicated Review page surfaces only what's currently due, evaluates new attempts, and recalculates the next review date automatically.

### 📈 Personalized Dashboard
At a glance: total materials, total questions, total attempts, average score, questions due today, mastered vs. weak questions, overall accuracy, and upcoming reviews.

### 👤 Multi-User Data Isolation
Student A's materials, questions, attempts, and stats are completely invisible to Student B — enforced at the database query level via the authenticated user ID.

---

## 🏗️ System Architecture

```
                     ┌──────────────────────┐
                     │       Student         │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │  Google Login (OAuth) │
                     └──────────┬───────────┘
                                │
                          Unique User ID
                                │
                                ▼
                     ┌──────────────────────┐
                     │ Study Material Upload │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │  PDF Processor        │
                     │  (PyMuPDF)             │
                     └──────────┬───────────┘
                                │
                   ┌────────────┴────────────┐
                   ▼                         ▼
              Page Count                Text Extraction
                   │                         │
                   ▼                         │
            Question Count                   │
                   └────────────┬────────────┘
                                ▼
                     ┌──────────────────────┐
                     │   AI Engine (Gemini)  │
                     └──────────┬───────────┘
                                ▼
                       Generated Questions
                                ▼
                     ┌──────────────────────┐
                     │   SQLite Database     │
                     └──────────┬───────────┘
                                │
         ┌──────────────────────┼──────────────────────┐
         ▼                      ▼                      ▼
  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
  │     Quiz     │      │    Review    │      │  Dashboard   │
  └──────┬───────┘      └──────┬───────┘      └──────┬───────┘
         ▼                     ▼                     ▼
   Answer Check          Spaced Repetition       Analytics
```

---

## 🗄️ Database Design

SQLite with three core tables, linked by ID:

```
User ──▶ Materials ──▶ Questions ──▶ Attempts
```

<details>
<summary><b>Table schemas</b></summary>

**materials**
`material_id` · `user_id` · `filename` · `upload_date`

**questions**
`question_id` · `material_id` · `topic` · `question_type` · `question_text` · `options_json` · `correct_answer` · `last_attempt` · `last_score` · `attempt_count` · `next_review_date`

**attempts**
`attempt_id` · `question_id` · `user_answer` · `score` · `feedback` · `answered_at`

</details>

---

## 🧩 Core Modules

| Module | Responsibility |
|---|---|
| `core/auth.py` | Google authentication, login state, logout |
| `core/db.py` | SQLite connection, schema init/migration, CRUD for materials/questions/attempts |
| `core/ai_engine.py` | AI question generation, short-answer evaluation, feedback |
| `core/pdf_processor.py` | PDF processing and text extraction |
| `core/scheduler.py` | Spaced-repetition scheduling, next review date |
| `core/schemas.py` | Structured data models for the AI engine |

## 🖥️ Application Pages

| Page | What it does |
|---|---|
| **Study Material** | Upload & process PDFs, count pages, generate & store questions |
| **Quiz** | Select material, display questions, collect & evaluate answers, save attempts |
| **Review** | Surface due questions, re-evaluate, update review schedules |
| **Dashboard** | Progress stats — accuracy, mastered/weak questions, upcoming reviews |

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Language | Python |
| Frontend | Streamlit |
| AI Model | Google Gemini |
| Authentication | Google OAuth 2.0 / OpenID Connect |
| PDF Processing | PyMuPDF |
| Database | SQLite |
| Data Validation | Pydantic |
| Config | python-dotenv |
| VCS | Git / GitHub |

---

## 📁 Project Structure

```
ai-study-buddy/
├── app.py
├── README.md
├── LICENSE
├── requirements.txt
├── .env / .env.example
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
```

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/mahesh96-hub/ai-study-buddy.git
cd ai-study-buddy
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root:
```bash
GEMINI_API_KEY=your_gemini_api_key
```
> ⚠️ Never commit `.env` to GitHub.

**5. Configure Google Authentication**

Create `.streamlit/secrets.toml`:
```toml
[auth]
redirect_uri = "http://localhost:8501/oauth2callback"
cookie_secret = "YOUR_RANDOM_SECRET"
client_id = "YOUR_GOOGLE_CLIENT_ID"
client_secret = "YOUR_GOOGLE_CLIENT_SECRET"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```
> ⚠️ Never commit `.streamlit/secrets.toml` to GitHub. For production, update `redirect_uri` to your deployed OAuth callback URL.

**6. Run the app**
```bash
streamlit run app.py
```

---

## 🧪 Testing Checklist

| Test | Flow |
|---|---|
| Authentication | Google Login → Authenticated → user-specific app |
| PDF Processing | Upload → Page Count → Question Count → Generation |
| Quiz | Select Material → Answer → Submit → Score + Feedback |
| Review | Due Question → Review → New Score → New Review Date |
| User Isolation | Student A uploads & logs out → Student B logs in → A's material must **not** appear |

---

## 🔒 Security Considerations

- **Authentication** — Google OAuth is used instead of storing passwords in the app.
- **User Isolation** — every database query is scoped to the authenticated user's ID.
- **Secrets Protection** — `GEMINI_API_KEY` and OAuth credentials live in `.env` / `.streamlit/secrets.toml`, both git-ignored.
- **Data Relationships** — `User → Material → Question → Attempt` ensures nothing crosses user boundaries.

---

## 📈 Example Learning Scenario

1. A student uploads `Cyber Security Unit 1.pdf` (18 pages).
2. The system determines **15 questions** are needed and generates them with Gemini.
3. The student takes the quiz; answers are evaluated and scored.
4. The attempt is stored and the next review date is scheduled.
5. When the review comes due, the student answers again — performance updates, the review date recalculates, and the dashboard refreshes automatically.

---

## 🌟 Why AI Study Buddy?

Most learning tools stop at content delivery. AI Study Buddy covers the **full loop**:

```
Study → Practice → Evaluate → Review → Track → Improve
```

Every student and every topic is treated differently — because they aren't the same.

---

## 📌 Current Project Status

✅ Google Authentication · ✅ Multi-user data isolation · ✅ Multiple PDF upload · ✅ PDF page counting
✅ Adaptive question generation · ✅ Independent material processing · ✅ AI question generation
✅ MCQ / True-False evaluation · ✅ AI short-answer evaluation · ✅ Quiz scoring · ✅ Attempt tracking
✅ Spaced repetition · ✅ Review system · ✅ Personalized dashboard · ✅ Upcoming review tracking

🔮 Future Scope

File Support

DOCX / PPTX / TXT
Image / OCR materials
Scanned PDF support

Learning Intelligence

Automatic topic extraction
Difficulty-level selection
Weak-topic detection
Personalized difficulty

Analytics

Performance graphs
Subject-wise progress
Weekly study trends
Learning streaks

Platform

Flashcards
Cloud database support
Mobile-friendly UI
Production deployment
