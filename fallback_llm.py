from langchain_groq import ChatGroq
import os

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)

def ask_llm(prompt: str) -> str:
    return llm.invoke(prompt).content
