from crewai import Task
from textwrap import dedent
from job_manager import append_task_output, append_event
from utils.logging import logger


class TravelTasks:
    def __init__(self, job_id):
        self.job_id = job_id

    def append_event_callback(self, task_name, task_output):
        logger.info("Callback called: %s", task_output)
        append_event(self.job_id, task_name + " has been finished")
        append_task_output(self.job_id, task_output.exported_output, task_name)

    def identify_task(self, agent, origin, cities, interests, range):
        task_name = "identify_task"
        return Task(
            description=dedent(
                f"""Analyze and select the best city for the trip based on specific criteria such as weather patterns, seasonal events, and travel costs. This task involves comparing multiple cities, considering factors like current weather conditions, upcoming cultural or seasonal events, and overall travel expenses. Your final answer must be a detailed report on the chosen city, and everything you found out about it, including the flight information such as flight cost, airline options, flight duration, weather forecast and attractions.

                Traveling from: {origin}
                City Options: {cities}
                Trip Date: {range}
                Traveler Interests: {interests}
                
                {self.__important(cities)}
                """
            ),
            agent=agent,
            expected_output=dedent("""Markdown"""),
            callback=lambda task_output: self.append_event_callback(
                task_name, task_output
            ),
        )

    def gather_task(self, agent, origin, cities, interests, range):
        # task_name = "gather_task"
        return Task(
            description=dedent(
                f"""As a local expert on this city you must compile a city guide information for someone traveling there and wanting to have THE BEST trip ever!. Gather information about top attractions, local customs, special events, and daily activity recommendations. Find the best spots to go to, the kind of place only a local would know. This guide should provide a thorough overview of what the city has to offer, including hidden gems, cultural hotspots, must-visit landmarks, weather forecasts, and high level costs. The final answer must be a comprehensive city guide, rich in cultural insights and practical tips, tailored to enhance the travel experience.

                Trip Date: {range}
                Traveling from: {origin}
                City Options: {cities}
                Traveler Interests: {interests}
                
                {self.__important(cities)}
                5. You CANNOT provide images in your answer."""
            ),
            agent=agent,
            expected_output=dedent("""Markdown"""),
        )

    def illustrate_task(self, agent):
        task_name = "gather_task"
        return Task(
            description=dedent(
                f"""As an Image search expert You are expert in searching for the best images from \"Bing Image Search\". You MUST take all city guide information from Local Expert at this city and update it following the rules below.
                1. You MUST search and insert the image of each item in the list of \"Top Attractions\" from \"Bing Image Search\". *** Only one image per item ***.
                2. Do not insert anything to the item that you cannot find the image from \"Bing Image Search\" for it.
                3. You final answer MUST contain the full detail of city guide information that you received from local expert.
                """
            ),
            agent=agent,
            expected_output=dedent("""Markdown with text and images"""),
            callback=lambda task_output: self.append_event_callback(
                task_name, task_output
            ),
        )

    def plan_task(self, agent, origin, cities, interests, range):
        task_name = "plan_task"
        return Task(
            description=dedent(
                f"""Expand this guide into a travel itinerary with detailed per-day plans, including weather forecasts, places to eat, packing suggestions, and a budget breakdown. You MUST suggest actual places to visit, actual hotels to stay and actual restaurants to go to. This itinerary should cover all aspects of the trip, from arrival to departure, integrating the city guide information with practical travel logistics. Your final answer MUST be a complete expanded travel plan, encompassing a daily schedule, anticipated weather conditions, recommended clothing and items to pack, and a detailed budget, ensuring THE BEST TRIP EVER.

                Trip Date: {range}
                Traveling from: {origin}
                City Options: {cities}
                Traveler Interests: {interests}
                
                {self.__important(cities)}"""
            ),
            agent=agent,
            expected_output=dedent("""Markdown"""),
            callback=lambda task_output: self.append_event_callback(
                task_name, task_output
            ),
        )

    def __important(self, cities):
        return f"""To do this task, you understand the following instruction:
        1. If you want to find an information about weather you can searching the internet using the word that start with \"Accuweather\" and appending it with the city name and month for which you want to know weather information.
        2. You can use the popular websites such as \"Wanderlog\" or \"TripAdvisor\" to find many information about that city in the month you visited. For Example \"Wanderlog - {cities} in August\".
        3. Output only the full detail, without any additional comments.
        4. Your content topic should highlight with bold text.
        """
