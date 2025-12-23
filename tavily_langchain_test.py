from tavily import TavilyClient

# Initialize client
client = TavilyClient()


print("\n== 1. BASIC SEARCH ==\n")
basic_search = client.search("What is LangChain?")
print(basic_search)


print("\n 2. DIRECT ANSWER (Using include_answer=True) \n")
direct_answer = client.search(
    query="Explain the purpose of LangGraph",
    include_answer=True
)
print("Answer:", direct_answer.get("answer"))


print("\n3. ADVANCED SEARCH\n")
advanced_search = client.search(
    query="Latest updates in AI agents",
    include_answer=True,
    max_results=5
)
print("Answer:", advanced_search.get("answer"))
print("Sources:")
for item in advanced_search.get("results", []):
    print("-", item.get("url"))


print("\n4. FOLLOW-UP QUESTIONS\n")
follow_up = client.search(
    query="What is Generative AI?",
    include_answer=True,
    include_follow_up_questions=True
)
print("Main Answer:", follow_up.get("answer"))
print("Follow-up Questions:", follow_up.get("follow_up_questions"))


print("\n 5. SUMMARY API =====================\n")
summary_result = client.summary("Give a short summary of LangChain")
print("Summary:", summary_result.get("summary"))


print("\n===================== TASK COMPLETED SUCCESSFULLY =====================\n")
