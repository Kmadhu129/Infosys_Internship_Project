from pydantic import BaseModel
from typing import List, Dict


class ResearchState(BaseModel):
    query: str
    history: List[str]
    sub_questions: List[str]
    search_results: Dict[str, str]
    plan: str = ""
    final_answer: str = ""
