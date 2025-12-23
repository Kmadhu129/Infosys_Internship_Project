import fitz
from langchain_groq import ChatGroq
import os
import requests

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)

def summarize_pdf(file, length):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = "".join(page.get_text() for page in doc)

    prompt = f"Give a {length} summary:\n{text}"
    return llm.invoke(prompt).content

def summarize_url(url, length):
    content = requests.get(url).text
    prompt = f"Give a {length} summary of this webpage:\n{content}"
    return llm.invoke(prompt).content
