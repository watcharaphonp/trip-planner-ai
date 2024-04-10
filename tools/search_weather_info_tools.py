from langchain.tools import tool
from crewai import Agent, Task
from configs.model import Models
from textwrap import dedent


class WeatherSearchTools:

    @tool(
        "Summarize a weather information and weather forecast information from website url"
    )
    def summarize_weather_info_from_web(website_url):
        """Summarize a weather information and weather forecast information from a given website url"""
        model_configs = Models.claude3Haiku()
        llm = model_configs["model"]
        max_rpm = model_configs["max_rpm"]
        max_iter = model_configs["max_iter"]
        summaries = []

        agent = Agent(
            role="Weather Researcher",
            goal="Do amazing researches and summaries weather information from website url",
            backstory="You're a Principal Researcher at a big company and you need to do research about weather information and weather forecast from given website url.",
            allow_delegation=False,
            llm=llm,
            max_rpm=max_rpm,
            max_iter=max_iter,
        )
        task = Task(
            agent=agent,
            description=f'Analyze and summarize the content from a given website url "{website_url}" and summarize a weather information and weather forecast information, make sure to include the most relevant information in the summary, return only the summary nothing else.',
            expected_output=dedent("""Text"""),
        )
        summary = task.execute()
        summaries.append(summary)

        return "\n\n".join(summaries)
