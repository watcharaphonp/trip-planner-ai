from langchain.tools import tool
from crewai import Agent, Task
from configs.model import Models
from textwrap import dedent


class SkyScannerTools:

    @tool(
        "Search, scrapping content and summarize flight information from SkyScanner Website"
    )
    def summarize_flight_info(
        departure_airport_code, destination_airport_code, arrival_date, return_date
    ):
        """Scrapping and summarizes flight information from SkyScanner Website according to following parameters
        departure_airport_code: Departure Airport Code such as BKK
        destination_airport_code: Destination Airport Code such as BKK
        arrival_date: Arrival Date in format YYMMDD Ex. 20 July 2024 => 240720
        return_date: Return Date in format YYMMDD Ex. 20 July 2024 => 240720
        """

        website_url = f"https://www.skyscanner.net/transport/flights/{departure_airport_code}/{destination_airport_code}/{arrival_date}/{return_date}"
        summaries = []

        model_configs = Models.bedrockHaiku()
        llm = model_configs["model"]
        max_rpm = model_configs["max_rpm"]
        max_iter = model_configs["max_iter"]

        agent = Agent(
            role="Flight Researcher",
            goal="Do amazing researches and summaries based on the flight information from given website url",
            backstory="You're a Flight Researcher at a big company and you need to do research about flight information.",
            allow_delegation=False,
            llm=llm,
            max_rpm=max_rpm,
            max_iter=max_iter,
        )
        task = Task(
            agent=agent,
            description=f'Analyze and summarize the content about Airline options, Flight duration, Roundtrip ticket prices range from a given website url "{website_url}", make sure to include the most relevant information in the summary, return only the summary nothing else.',
            expected_output=dedent("""Text"""),
        )
        summary = task.execute()
        summaries.append(summary)

        return "\n\n".join(summaries)
