import tavily
import re

def search_fraud_info(prompt: str, num_results: int = 5) -> str:
    """
    Searches the web for recent fraud-related information using Tavily
    and returns the first few results combined as a text summary.
    """
    # Step 1: Initialize the Tavilly search client
    client = tavily.Client()

    # Step 2: Perform a web search
    results = client.search(query=prompt, max_results=num_results, recent_days=14)

    if not results:
        return "No recent information found."

    sections = []
    for res in results:
        title = res.get('title', '[No title]')
        url = res.get('url')
        snippet = res.get('snippet', '')

        # Step 3: Optionally, follow the link and scrape full main content
        page = client.fetch(url)
        content = client.extract(page, selector='main') or client.extract(page, selector='article')
        content = content[:2000]  # limit length

        sections.append(f"[{title}] {snippet.strip()}\n{content.strip()}")

    # Step 4: Combine the sections into one text output
    combined = "\n\n---\n\n".join(sections)
    combined = re.sub(r'\s+', ' ', combined)  # normalize whitespace
    return combined