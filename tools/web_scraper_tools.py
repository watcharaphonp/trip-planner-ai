from langchain.tools import tool
from crewai import Agent, Task
from configs.model import Models
from textwrap import dedent


class WebScraperTools:
    def __init__(self, user_id):
        self.user_id = user_id

    @tool("Scrape website content")
    def scrape_and_summarize_website(self, website_url, topic):
        """Scrapes and summarizes a website's content according to given topics from website url"""
        summaries = []

        model_configs = Models.bedrockHaiku(self.user_id)
        llm = model_configs["model"]
        max_rpm = model_configs["max_rpm"]
        max_iter = model_configs["max_iter"]

        agent = Agent(
            role="Principal Researcher",
            goal="Do amazing researches and summaries based on the content from given website url",
            backstory="You're a Principal Researcher at a big company and you need to do research about a given topic.",
            allow_delegation=False,
            llm=llm,
            max_rpm=max_rpm,
            max_iter=max_iter,
        )
        task = Task(
            agent=agent,
            description=f'Analyze and summarize the content about "{topic}" from a given website url "{website_url}", make sure to include the most relevant information in the summary, return only the summary nothing else.',
            expected_output=dedent("""Text"""),
        )
        summary = task.execute()
        summaries.append(summary)

        return "\n\n".join(summaries)
