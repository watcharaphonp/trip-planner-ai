import json
import os

import requests
from langchain.tools import tool
from crewai import Agent, Task
from bs4 import BeautifulSoup


class BrowserTools:

    @tool("Scrape website content")
    def scrape_and_summarize_website(website_url):
        """Scrapes and summarizes a website's content using Beautiful Soup."""
        html_content = requests.get(website_url)
        soup = BeautifulSoup(html_content.text, "html.parser")
        # Extract elements or data from the soup object as needed
        elements = soup.find_all("p")  # Example: Find all paragraphs

        content = "\n\n".join([str(el) for el in elements])
        content = [content[i : i + 8000] for i in range(0, len(content), 8000)]
        summaries = []
        for chunk in content:
            agent = Agent(
                role="Principal Researcher",
                goal="Do amazing researches and summaries based on the content you are working with",
                backstory="You're a Principal Researcher at a big company and you need to do research about a given topic.",
                allow_delegation=False,
                max_rpm=3,
            )
            task = Task(
                agent=agent,
                description=f"Analyze and summarize the content below, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}",
            )
            summary = task.execute()
            summaries.append(summary)
        return "\n\n".join(summaries)
