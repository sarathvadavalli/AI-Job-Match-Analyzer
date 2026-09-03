# AI Resume & Job Description Analyzer

An AI-powered application that extracts structured information from resumes
and job descriptions using Large Language Model (LLM). The project is designed to eventually analyze a candidate's resume against a job description and provide meaningful insights about their compatibility.

## Current Status

### Completed

- Resume information extraction
- Job description information extraction
- LLM-based structured data extraction
- Pydantic-based response validation
- Modular project architecture

### Planned

- Resume and JD matching
- Skill matching and gap analysis
- Match score generation
- Candidate recommendations
- Database integration
- Frontend improvements

## Features

### Resume Extraction

Users can upload a resume, which is processed to extract structured
candidate information such as:

- Personal information
- Skills
- Education
- Work experience
- Projects
- Profile links

### Job Description Extraction

Users can upload a job description and extract structured information such as:

- Job title
- Required skills
- Preferred skills
- Experience requirements
- Education requirements
- Responsibilities
- Other job requirements

## Architecture

The application follows a modular architecture where each component is
responsible for a specific task.

```text
Document Upload
      │
      ▼
Text Extraction
      │
      ▼
LLM Extraction
      │
      ▼
Response Validation
      │
      ▼
Structured Data
```

## Project Structure

```text
JD_Extractor/
├── .env.example
├── .gitignore
├── curl_command.sh
├── README.md
├── requirements.txt
├── run.py
├── myapp/
│   ├── main.py
│   ├── routes.py
│   ├── schemas/
│   │   ├── job_extraction.py
│   │   ├── job_response.py
│   │   └── resume_extraction.py
│   ├── services/
│   │   ├── doc_service.py
│   │   ├── job_service.py
│   │   ├── resume_service.py
│   │   └── llm/
│   │       ├── client.py
│   │       └── context.py
│   └── templates/
│       ├── upload_jd.html
│       └── upload_resume.html
└── tests/
      ├── __init__.py
      ├── results.json
      ├── test_extraction.py
      └── testcases.json
```
