import json
import requests

from langchain.tools import tool


class DuckDuckGoSearchTools:
    @tool("Search the internet")
    def search_internet(query):
        """Useful to search the internet
        about a given topic and return relevant results"""
        top_result_to_return = 4
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json"}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return "Sorry, there was an error with the search request."

        results = response.json()["RelatedTopics"]
        string = []
        for result in results[:top_result_to_return]:
            try:
                string.append(
                    "\n".join(
                        [
                            f"Title: {result['Text']}",
                            f"Link: {result['FirstURL']}",
                            f"Snippet: {result['Result']}",
                            "\n-----------------",
                        ]
                    )
                )
            except KeyError:
                continue

        return "\n".join(string)
