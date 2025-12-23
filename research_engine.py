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


# ---------- GENERAL WEB ----------
def general_web_answer(prompt: str) -> str:
    response = llm.invoke(prompt)
    return response.content


# ---------- ACADEMIC PAPERS ----------
def research_paper_answer(prompt: str):
    """
    Uses Tavily to fetch academic content and answers strictly from it.
    Returns answer + reference links
    """

    search_results = tavily.search(
        query=prompt,
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

    final_prompt = f"""
You are an academic research assistant.

Answer ONLY using the provided research content.

Research Content:
{papers_text}

User Question:
{prompt}

Rules:
- If user asks for title → give title only
- If user asks for summary → summarize only that paper
- If user asks for methodology → extract methodology only
- Do NOT hallucinate
"""

    answer = llm.invoke(final_prompt).content

    return answer, references
