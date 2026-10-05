# AI Job Match Analyzer

AI-powered resume and job-description analysis for faster, evidence-based applications.

The application extracts structured candidate data, compares it with a job description, and returns a practical match report.

## Features

- **Authentication**: Authenticates the user with JWT technique by storing in a HttpOnly cookie.
- **Profile management**: Upload a resume and autofill the input fields of profile. Review and edit extracted information before saving.
- **Resume extraction**: Convert PDF, DOCX, or TXT resumes into structured profiles and store into Mongodb database.
- **Match analysis**: Compare a saved profile with a job description and generates insights from it.
- **Skill evidence**: Show matched skills with proficiency levels and supporting evidence.
- **Gap analysis**: Separate required and optional missing skills.
- **Actionable feedback**: Recommend focused improvements across skills, projects, experience, and education.

## User Flow

1. Register or sign in.
2. Upload a resume from the profile page for autofill.
3. Review and save the extracted profile.
4. Open **Match Analysis**.
5. Upload a job description or paste its text.
6. Review the score, strengths, gaps, and recommendations.

## Tech Stack

- **Backend**: FastAPI, Python
- **Authentication**: password hashing, JWT, HTTP-only cookies
- **Validation**: Pydantic
- **Templates**: Jinja2, HTML, CSS, JavaScript
- **Database**: MongoDB with PyMongo
- **Document parsing**: PyMuPDF, python-docx, optional Tesseract OCR
- **LLM**: Google Gemini through `google-genai`

## Quick Start

### Prerequisites

- Python 3.11 or newer
- MongoDB running locally or a reachable MongoDB deployment
- A Google Gemini API key
- Tesseract OCR for scanned PDFs

### Install

```bash
git clone <repository-url>
cd JD_Extractor
python -m venv .venv
```

Activate the virtual environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS or Linux
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Configure Environment

Create a `.env` file in the project root with the fields specified in `.env.example`

### Run

```bash
python run.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

FastAPI documentation is available at:

- [Swagger UI](http://127.0.0.1:8000/docs)
- [ReDoc](http://127.0.0.1:8000/redoc)

The sample match response is available in output.json.

## Architecture

```text
 Browser
   │
   ▼
FastAPI Routes
   │
   ├──────────────► AuthService ─────────► MongoDB
   │
   ├──────────────► ProfileService ──────► MongoDB
   │
   └──────────────► MatchService
                         │
                         ├──► DocumentService (For JD)
                         │       └── PDF / DOCX / TXT / OCR
                         |
                         ├──► Profile Data from MongoDB
                         |
                         ├──► Pydantic for Profile and Matching Schema
                         |
                         ├──► LLMClient
                         │       └── Gemini
                                  │
                                  ▼
                            Matching Result
```

## Project Structure

```text
JD_Extractor/
├── myapp/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── db.py
│   │   └── security.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── document_routes.py
│   │   └── page_routes.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── job_extraction.py
│   │   ├── job_match_result.py
│   │   ├── job_response.py
│   │   └── resume_extraction.py
│   ├── services/
│   │   ├── doc_service.py
│   │   ├── job_service.py
│   │   ├── match_service.py
│   │   ├── resume_service.py
│   │   └── llm/
│   │       ├── client.py
│   │       └── context.py
│   └── templates/
│       ├── analysis.html
│       ├── dashboard.html
│       ├── login.html
│       ├── profile.html
│       ├── profile_form.html
│       ├── upload_jd.html
│       └── upload_resume.html
├── tests/
├── requirements.txt
├── run.py
└── README.md
```

## Testing

Run the automated test suite with:

```bash
python -m tests.test_extraction
```

The extraction test workflow uses the cases in `tests/testcases.json` and writes results to `tests/results.json`.

## Improvements

- Developing an algorithm that could evaluate match score deterministically based on the weights of each skill representing its importance in job description.
- Creating an agentic workflow that could autonomously fetch job descriptions from job portals, calculate match scores and display the most relevant jobs that are suitable for a candidate.

## License
This project is licensed under the MIT License.
