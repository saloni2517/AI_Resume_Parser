import re
import fitz
from docx import Document
from pathlib import Path


def extract_text(file_path):
    """Extract text from PDF or DOCX resumes."""
    file_path = Path(file_path)
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        text = ""

        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text() + "\n"

        return text

    elif extension == ".docx":
        document = Document(file_path)

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

        return text

    else:
        raise ValueError("Only PDF and DOCX files are supported.")


def parse_resume(file_path):
    """Extract basic information and skills from a resume."""
    text = extract_text(file_path)

    # Extract email
    email_match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text
    )
    email = email_match.group(0) if email_match else "Not found"

    # Extract phone number
    phone_match = re.search(
        r"(?<!\w)(?:\+?\d{1,3}[-.\s]?)?"
        r"(?:\(?\d{3,5}\)?[-.\s]?)?\d{6,10}(?!\w)",
        text
    )
    phone = phone_match.group(0).strip() if phone_match else "Not found"

    # Estimate name from the first non-empty line
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    name = lines[0] if lines else "Not found"

    # Identify technical skills
    skill_list = [
        "Python", "Java", "C++", "C", "SQL",
        "HTML", "CSS", "JavaScript", "Flask",
        "React", "Node.js", "Machine Learning",
        "Data Science", "NumPy", "Pandas",
        "Scikit-learn", "TensorFlow", "AWS",
        "Git", "Linux", "MongoDB", "MySQL",
        "Deep Learning", "NLP"
    ]

    skills = []

    for skill in skill_list:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, re.IGNORECASE):
            skills.append(skill)

    # Identify education-related keywords
    education_keywords = [
        "B.Tech", "B.E.", "Bachelor",
        "Master", "M.Tech", "M.E.",
        "B.Sc", "M.Sc", "HSC", "SSC",
        "Diploma", "Ph.D"
    ]

    education = [
        keyword for keyword in education_keywords
        if re.search(re.escape(keyword), text, re.IGNORECASE)
    ]

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "resume_text": text
    }