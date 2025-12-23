from research_engine import general_web_answer, research_paper_answer
import re


def is_follow_up(query: str) -> bool:
    follow_up_keywords = [
        "summarize", "summary", "title", "methodology",
        "limitations", "advantages", "applications",
        "first paper", "second paper", "this paper",
        "that paper", "previous paper"
    ]
    q = query.lower()
    return any(k in q for k in follow_up_keywords)


def run_research(query, messages, mode):
    """
    query    : latest user input ONLY
    messages : full chat history
    mode     : General Web | Academic Papers
    """

    # ---- Build conversation context for LLM ----
    context_text = ""
    for m in messages:
        context_text += f"{m['role'].upper()}: {m['content']}\n"

    # ==========================
    # ACADEMIC PAPERS MODE
    # ==========================
    if mode == "Academic Papers":

        # 🔑 FOLLOW-UP QUESTION → NO TAVILY
        if is_follow_up(query):
            prompt = f"""
You are an academic research assistant.

Conversation context:
{context_text}

User follow-up question:
{query}

Rules:
- Answer ONLY from previously discussed papers
- Do NOT search the web
- Do NOT introduce new papers
- Be precise and concise
"""
            answer = general_web_answer(prompt)
            return answer, []

        # 🔑 FIRST ACADEMIC QUERY → USE TAVILY
        return research_paper_answer(query)

    # ==========================
    # GENERAL WEB MODE
    # ==========================
    prompt = f"""
Conversation so far:
{context_text}

User question:
{query}

Rules:
- Answer clearly
- Use previous context if needed
"""
    answer = general_web_answer(prompt)
    return answer, []
