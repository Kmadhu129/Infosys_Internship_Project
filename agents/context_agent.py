class ContextAgent:
    def resolve(self, question: str, papers: list):
        q = question.lower()

        # paper number reference
        for i, p in enumerate(papers):
            if f"paper {i+1}" in q or f"{i+1}st paper" in q:
                return p

        # url reference
        for p in papers:
            if p["url"] in question:
                return p

        return None
