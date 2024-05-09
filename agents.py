from crewai import Agent
from tools.search_duckduckgo_tools import DuckDuckGoSearchTools
from tools.web_scraper_tools import WebScraperTools
from tools.calculator_tools import CalculatorTools
from tools.sky_scanner_tools import SkyScannerTools
from configs.model import Models
from tools.image_search_tools import ImageSearchTools


class TravelAgents:

    def __init__(self, user_id, session_id):
        self.model_configs = Models.bedrockHaiku(user_id, session_id)
        self.llm = self.model_configs["model"]
        self.max_rpm = self.model_configs["max_rpm"]
        self.max_iter = self.model_configs["max_iter"]
        self.user_id = user_id
        self.session_id = session_id

    def city_selection_agent(self):
        webScraperTools = WebScraperTools(self.user_id, self.session_id)
        skyScannerTools = SkyScannerTools(self.user_id, self.session_id)
        return Agent(
            role="City Selection Expert",
            goal="Select the best city based on weather, season, and prices",
            backstory="An expert in analyzing travel data to pick ideal destinations",
            tools=[
                DuckDuckGoSearchTools.search_internet,
                webScraperTools.scrape_and_summarize_website,
                skyScannerTools.summarize_flight_info,
            ],
            llm=self.llm,
            verbose=True,
            max_rpm=self.max_rpm,
            max_iter=self.max_iter,
        )

    def local_expert(self):
        webScraperTools = WebScraperTools(self.user_id, self.session_id)
        skyScannerTools = SkyScannerTools(self.user_id, self.session_id)
        return Agent(
            role="Local Expert at this city",
            goal="Provide the BEST insights about the selected city",
            backstory="""A knowledgeable local guide with extensive information about the city, it's attractions and customs""",
            tools=[
                DuckDuckGoSearchTools.search_internet,
                webScraperTools.scrape_and_summarize_website,
                skyScannerTools.summarize_flight_info,
            ],
            llm=self.llm,
            verbose=True,
            max_rpm=self.max_rpm,
            max_iter=self.max_iter,
        )

    def image_search_expert(self):
        return Agent(
            role="Image search expert",
            goal="Provide the BEST images for the city guide information from local expert at this city",
            backstory="""A knowledgeable about searching for photos from the Bing Image Search.""",
            tools=[
                ImageSearchTools.search_image,
            ],
            llm=self.llm,
            verbose=True,
            max_rpm=self.max_rpm,
            max_iter=self.max_iter,
        )

    def travel_concierge(self):
        webScraperTools = WebScraperTools(self.user_id, self.session_id)
        skyScannerTools = SkyScannerTools(self.user_id, self.session_id)
        return Agent(
            role="Amazing Travel Concierge",
            goal="""Create the most amazing travel itineraries with budget and packing suggestions for the city""",
            backstory="""Specialist in travel planning and logistics with decades of experience""",
            tools=[
                DuckDuckGoSearchTools.search_internet,
                webScraperTools.scrape_and_summarize_website,
                skyScannerTools.summarize_flight_info,
                CalculatorTools.calculate,
            ],
            llm=self.llm,
            verbose=True,
            max_rpm=self.max_rpm,
            max_iter=self.max_iter,
        )
