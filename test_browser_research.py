from research.browser_agent import search_google

query = "Bitcoin ETF approval news"
results = search_google(query)

for i, result in enumerate(results, 1):
    print(f"\n🔗 Result {i}:")
    print("Title:", result["title"])
    print("Link:", result["link"])
    print("Snippet:", result["snippet"])
