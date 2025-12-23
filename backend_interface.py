from research_engine import general_web_answer, research_paper_answer


def run_research(query, messages, mode):
    """
    query    : current user question
    messages : full chat history (for context)
    mode     : General Web | Academic Papers
    """

    # ---- Build conversational context ----
    context_text = ""
    for m in messages:
        role = m["role"].upper()
        content = m["content"]
        context_text += f"{role}: {content}\n"

    # ---- Combine context + new question ----
    final_query = f"""
You are a research assistant.

Conversation so far:
{context_text}

User question:
{query}

Rules:
- Use previous context if the question refers to earlier answers
- If user refers to paper numbers, titles, links, summarize or extract ONLY from those
- Do not add unrelated information
"""

    # ---- Route by mode ----
    if mode == "Academic Papers":
        answer, refs = research_paper_answer(final_query)
    else:
        answer = general_web_answer(final_query)
        refs = []

    return answer, refs
