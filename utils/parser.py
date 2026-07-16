import re

import pdfplumber

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
PHONE_PATTERN = re.compile(r"(?:\+?\d{1,3}[\s\-.]?)?(?:\(?\d{2,4}\)?[\s\-.]?){2,4}\d{2,4}")


def extract_text(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def extract_email(text):
    match = EMAIL_PATTERN.search(text)
    return match.group(0) if match else ""


def extract_phone(text):
    for candidate in PHONE_PATTERN.findall(text):
        digits = re.sub(r"\D", "", candidate)
        if 10 <= len(digits) <= 13:
            return candidate.strip()
    return ""


def extract_name(text):
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if "@" in line or any(char.isdigit() for char in line):
            continue
        words = line.split()
        if 1 <= len(words) <= 4 and all(word.replace(".", "").isalpha() for word in words):
            return line.title()
    return "Unknown Candidate"


def parse_resume(filepath):
    text = extract_text(filepath)
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "text": text,
    }
