from crewai import Agent
from tools.search_tools import SearchTools
from tools.search_duckduckgo_tools import DuckDuckGoSearchTools
from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from typing import List
from langchain_community.chat_models import ChatLiteLLM


class TravelAgents:

    def __init__(self):
        # Set LLM
        self.llm = ChatLiteLLM(model="claude-3-haiku-20240307", max_tokens=4096)

    def city_selection_agent(self):
        return Agent(
            role="City Selection Expert",
            goal="Select the best city based on weather, season, and prices",
            backstory="An expert in analyzing travel data to pick ideal destinations",
            tools=[
                DuckDuckGoSearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
            ],
            llm=self.llm,
            verbose=True,
        )

    def local_expert(self):
        return Agent(
            role="Local Expert at this city",
            goal="Provide the BEST insights about the selected city",
            backstory="""A knowledgeable local guide with extensive information
            about the city, it's attractions and customs""",
            tools=[
                DuckDuckGoSearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
            ],
            llm=self.llm,
            verbose=True,
        )

    def travel_concierge(self):
        return Agent(
            role="Amazing Travel Concierge",
            goal="""Create the most amazing travel itineraries with budget and 
            packing suggestions for the city""",
            backstory="""Specialist in travel planning and logistics with 
            decades of experience""",
            tools=[
                DuckDuckGoSearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
                CalculatorTools.calculate,
            ],
            llm=self.llm,
            verbose=True,
        )
