import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
from PyPDF2 import PdfReader
from docx import Document

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(
    page_title="AI Career Assistant Agent",
    layout="wide"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "latest_result" not in st.session_state:
    st.session_state.latest_result = ""


def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf_reader = PdfReader(uploaded_file)

    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def extract_match_score(text):
    match = re.search(r"(\d{1,3})\s*%", text)
    if match:
        score = int(match.group(1))
        return min(score, 100)
    return 0


def run_ai_agent(task_name, prompt):
    with st.spinner(f"Running {task_name}..."):
        response = model.generate_content(prompt)
        result = response.text

        st.session_state.latest_result = result

        st.session_state.chat_history.append({
            "task": task_name,
            "response": result
        })

        st.success(f"{task_name} Complete!")
        st.markdown(result)

        st.download_button(
            label=f"Download {task_name} Output",
            data=result,
            file_name=f"{task_name.replace(' ', '_').lower()}.txt",
            mime="text/plain"
        )

        return result


st.sidebar.title("AI Career Assistant")

menu = st.sidebar.radio(
    "Choose Tool",
    [
        "Resume Match",
        "Resume Rewrite",
        "Job Application Email",
        "Interview Prep",
        "LinkedIn Summary",
        "Agent Memory"
    ]
)

if st.sidebar.button("Clear Agent Memory"):
    st.session_state.chat_history = []
    st.session_state.latest_result = ""
    st.sidebar.success("Memory cleared.")

st.title("AI Career Assistant Agent")
st.write("Upload your resume and paste a job description to generate career-focused AI outputs.")

with st.container():
    st.subheader("Input Section")

    uploaded_resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"]
    )

    resume_text = ""

    if uploaded_resume:
        if uploaded_resume.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_resume)
        elif uploaded_resume.name.endswith(".docx"):
            resume_text = extract_text_from_docx(uploaded_resume)

        st.success("Resume uploaded successfully.")

        with st.expander("View Extracted Resume Text"):
            st.text_area("Extracted Resume Text", resume_text, height=250)

    job_description = st.text_area("Paste the Job Description Here", height=250)


st.divider()

if menu == "Agent Memory":
    st.subheader("Agent Memory / Previous Responses")

    if st.session_state.chat_history:
        for item in reversed(st.session_state.chat_history):
            with st.expander(item["task"]):
                st.markdown(item["response"])

                st.download_button(
                    label=f"Download {item['task']}",
                    data=item["response"],
                    file_name=f"{item['task'].replace(' ', '_').lower()}.txt",
                    mime="text/plain"
                )
    else:
        st.info("No AI responses generated yet.")

else:
    if resume_text and job_description:

        if menu == "Resume Match":
            st.subheader("Resume Match Analysis")

            st.info("This tool compares your resume with the job description and gives an ATS-style match score.")

            if st.button("Run Resume Match Analysis"):
                prompt = f"""
                You are an expert ATS resume reviewer.

                Compare the resume with the job description.

                Resume:
                {resume_text}

                Job Description:
                {job_description}

                Return the output exactly in this format:

                ## Match Percentage
                Give one estimated match percentage like 75%.

                ## Strong Matching Skills
                List the strongest matching skills.

                ## Missing Skills
                List important missing skills.

                ## ATS Improvement Suggestions
                Give practical resume improvement suggestions.

                ## Final Recommendation
                Explain whether the candidate is a strong, moderate, or weak fit.
                """

                result = run_ai_agent("Resume Match Analysis", prompt)

                score = extract_match_score(result)

                if score > 0:
                    st.subheader("ATS Score Card")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Resume Match Score", f"{score}%")

                    with col2:
                        if score >= 75:
                            st.metric("Fit Level", "Strong")
                        elif score >= 55:
                            st.metric("Fit Level", "Moderate")
                        else:
                            st.metric("Fit Level", "Weak")

                    with col3:
                        st.metric("Recommendation", "Optimize Resume")

                    st.progress(score / 100)

        elif menu == "Resume Rewrite":
            st.subheader("Resume Rewrite")

            st.info("This tool rewrites your resume content using ATS-friendly language.")

            if st.button("Rewrite Resume"):
                prompt = f"""
                You are a professional resume writer.

                Rewrite the resume content to better match the job description.

                Resume:
                {resume_text}

                Job Description:
                {job_description}

                Return the output in this format:

                ## Improved Professional Summary
                Write a short ATS-friendly summary.

                ## Rewritten Resume Bullet Points
                Rewrite 5 to 8 strong bullet points using action verbs, measurable impact, and job-relevant keywords.

                ## Keywords to Add
                List important keywords from the job description.

                ## Resume Positioning Advice
                Explain how the candidate should position their experience.
                """

                run_ai_agent("Resume Rewrite", prompt)

        elif menu == "Job Application Email":
            st.subheader("Job Application Email Generator")

            st.info("This tool creates a professional email from you to the recruiter or hiring manager.")

            recruiter_name = st.text_input("Recruiter / Hiring Manager Name", placeholder="Example: John")
            company_name = st.text_input("Company Name", placeholder="Example: Riddell")
            role_name = st.text_input("Role Name", placeholder="Example: Data Analyst")

            if st.button("Generate Job Application Email"):
                prompt = f"""
                You are helping a job seeker write a recruiter outreach email.

                Candidate Resume:
                {resume_text}

                Target Job Description:
                {job_description}

                Recruiter or Hiring Manager Name:
                {recruiter_name}

                Company Name:
                {company_name}

                Role Name:
                {role_name}

                Write a professional email FROM the candidate TO the recruiter or hiring manager.

                Requirements:
                - Humanized tone
                - Professional but not overly formal
                - Short and concise
                - Mention interest in the role
                - Mention relevant skills/background briefly
                - Mention attached resume
                - End politely
                - If recruiter name is blank, use a general greeting like "Hi,"
                - If company name or role name is blank, infer from the job description if possible

                Return:
                1. Subject line
                2. Full email
                """

                run_ai_agent("Job Application Email", prompt)

        elif menu == "Interview Prep":
            st.subheader("Interview Preparation")

            st.info("This tool generates likely interview questions and preparation topics.")

            if st.button("Generate Interview Questions"):
                prompt = f"""
                You are an interview coach.

                Based on the resume and job description, generate interview preparation material.

                Resume:
                {resume_text}

                Job Description:
                {job_description}

                Return the output in this format:

                ## Likely Interview Questions
                Give 10 likely questions.

                ## Technical Questions
                Give 5 technical questions.

                ## Behavioral Questions
                Give 5 behavioral questions.

                ## Topics to Prepare
                List important areas to revise.

                ## Candidate Talking Points
                Give strong talking points based on the resume.
                """

                run_ai_agent("Interview Preparation", prompt)

        elif menu == "LinkedIn Summary":
            st.subheader("LinkedIn Summary Generator")

            st.info("This tool creates LinkedIn headline, About section, and profile tips.")

            if st.button("Generate LinkedIn Summary"):
                prompt = f"""
                Create LinkedIn profile content based on the resume and job description.

                Resume:
                {resume_text}

                Job Description:
                {job_description}

                Return the output in this format:

                ## LinkedIn Headline
                Create a strong headline.

                ## LinkedIn About Section
                Write a natural, professional About section.

                ## Top Skills
                List important LinkedIn skills.

                ## Profile Improvement Tips
                Suggest improvements for LinkedIn visibility.
                """

                run_ai_agent("LinkedIn Summary", prompt)

    else:
        st.warning("Please upload a resume and paste a job description first.")