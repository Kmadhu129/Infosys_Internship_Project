from tavily import TavilyClient

client = TavilyClient(api_key=None)  # Will automatically use env var TAVILY_API_KEY

response = client.search("What is LangChain?")
print(response)
