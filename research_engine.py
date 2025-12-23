import os
import re
import requests
from bs4 import BeautifulSoup
from langchain_groq import ChatGroq
from tavily import TavilyClient

# ---------- API KEYS ----------
GROQ_KEY = os.getenv("GROQ_API_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")

llm = ChatGroq(
    api_key=GROQ_KEY,
    model="llama-3.1-8b-instant"
)

tavily = TavilyClient(api_key=TAVILY_KEY)


# ---------- UTILS ----------
def is_url(text: str) -> bool:
    return bool(re.match(r"https?://", text.strip()))


def extract_url_content(url: str) -> str:
    try:
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        text = " ".join(p.get_text(strip=True) for p in soup.find_all("p")[:60])
        return text
    except Exception:
        return ""


# ---------- GENERAL WEB ----------
def general_web_answer(prompt: str) -> str:
    return llm.invoke(prompt).content


# ---------- ACADEMIC PAPERS ----------
def research_paper_answer(query: str):
    """
    Handles BOTH:
    - topic-based academic search
    - direct paper URL analysis
    """

    # ✅ CASE 1: USER PASTED A URL
    if is_url(query):
        content = extract_url_content(query)

        if not content:
            return "Unable to extract content from the given URL.", []

        prompt = f"""
You are an academic research assistant.

Analyze ONLY the following paper content.

Content:
{content}

User request:
{query}

Rules:
- Answer strictly from this content
- Do not hallucinate
"""

        answer = llm.invoke(prompt).content
        return answer, [query]

    # ✅ CASE 2: NORMAL ACADEMIC SEARCH
    search_results = tavily.search(
        query=f"{query} research paper",
        max_results=3,
        search_depth="advanced"
    )

    papers_text = ""
    references = []

    for r in search_results.get("results", []):
        title = r.get("title", "")
        content = r.get("content", "")
        url = r.get("url", "")

        papers_text += f"\nTITLE: {title}\nCONTENT: {content}\n"
        if url:
            references.append(url)

    if not papers_text.strip():
        return "No relevant academic papers found.", []

    prompt = f"""
You are an academic research assistant.

Answer ONLY using the provided research content.

Research Content:
{papers_text}

User Question:
{query}

Rules:
- If user asks for title → give title only
- If user asks for methodology → give methodology only
- If user asks for limitations → give limitations only
- Do not add extra information
"""

    answer = llm.invoke(prompt).content
    return answer, references
