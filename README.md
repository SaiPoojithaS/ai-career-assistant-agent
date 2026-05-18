# AI Career Assistant Agent

An AI-powered career assistant built using Python, Streamlit, and Google Gemini API.

This application helps job seekers optimize resumes, generate recruiter outreach emails, prepare for interviews, and improve LinkedIn profiles using Generative AI workflows.

---

# Live Application

https://ai-career-assistant-agent-nhs6zplhezrsryqxcjq8gj.streamlit.app/

---

# Features

## Resume Match Analysis
- ATS-style resume matching
- Match percentage scoring
- Missing skills identification
- Resume optimization suggestions

## Resume Rewrite
- ATS-friendly bullet point rewriting
- Professional summary generation
- Keyword optimization
- Resume positioning guidance

## Job Application Email Generator
- Humanized recruiter outreach emails
- Professional email formatting
- Role-specific email generation

## Interview Preparation
- Technical interview questions
- Behavioral interview questions
- Preparation topics
- Candidate talking points

## LinkedIn Summary Generator
- LinkedIn headline generation
- About section generation
- Skill recommendations
- Profile optimization tips

## Agent Memory
- Stores previous AI outputs
- Downloadable generated responses

---

# Tech Stack

- Python
- Streamlit
- Google Gemini API
- Prompt Engineering
- PyPDF2
- python-docx

---

# Project Architecture

```text
User Resume Upload
        ↓
Resume Text Extraction
        ↓
Job Description Input
        ↓
AI Prompt Processing
        ↓
Gemini API Response
        ↓
Structured Career Output
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/SaiPoojithaS/ai-career-assistant-agent.git
```

## Navigate to Project

```bash
cd ai-career-assistant-agent
```

## Install Requirements

```bash
pip install -r requirements.txt
```

## Create .env File

```env
GEMINI_API_KEY=your_api_key_here
```

## Run Application

```bash
python -m streamlit run app.py
```

---

# Future Improvements

- Multi-agent orchestration
- RAG-based resume analysis
- Vector database integration
- Resume PDF export
- Cover letter generation
- AI chat assistant
- Job recommendation engine

---

# Author

Sai Siddaraju Poojitha
