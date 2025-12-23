from PyPDF2 import PdfReader
from langchain_groq import ChatGroq
import os

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)

def run_pdf_summary(pdf, length):
    reader = PdfReader(pdf)
    text = "".join(p.extract_text() or "" for p in reader.pages)

    return llm.invoke(
        f"Give a {length.lower()} summary:\n{text}"
    ).content
