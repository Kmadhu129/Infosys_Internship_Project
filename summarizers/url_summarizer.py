import requests
from bs4 import BeautifulSoup
from langchain_groq import ChatGroq
import os

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)

def run_url_summary(url, length):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    text = " ".join(
        p.get_text(strip=True)
        for p in soup.find_all("p")[:50]
    )

    return llm.invoke(
        f"Give a {length.lower()} summary:\n{text}"
    ).content
