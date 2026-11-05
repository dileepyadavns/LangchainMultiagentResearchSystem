from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv
from rich import print
from tavily import TavilyClient
load_dotenv()
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def scrap_url(url: str) -> str:
    """Scrap and extract clean readable content from a URL uses multiple extraction strategies for better results."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "accept_language": "en-US,en;q=0.9",
        "referer": "https://www.google.com/"
    }
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        html_content = response.text
        doc = Document(html_content)
        readable_html = doc.summary()
        text_content = trafilatura.extract(readable_html)
        if not text_content:
            return "Could not extract readable content from the URL."
        return text_content
    except (requests.RequestException, ValueError) as e:
        print(f"[red]Error during URL scraping: {e}[/red]")
        return "An error occurred while scraping the URL."
@tool
def websearch(query):
    """Perform a web search using Tavily API."""
    try:
        results = tavily.search(query=query, max_results=5)
        formatted_results = []
        for result in results.get("results", []):
            formatted_results.append(
                f"Title: {result.get('title', '')}\n"
                f"URL: {result.get('url', '')}\n"
                f"Snippet: {result.get('content', '')}"
            )
        return "\n\n".join(formatted_results) or "No search results found."
    except Exception as e:
        print(f"[red]Error during web search: {e}[/red]")
        return "An error occurred while performing the web search."
 