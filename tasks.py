from crewai import Task, Agent
from textwrap import dedent
from job_manager import append_task_output, append_event
from utils.logging import logger
import markdown
import json


class TravelTasks:
    def __init__(self, job_id):
        self.job_id = job_id

    def append_event_callback(self, task_name, task_output):
        logger.info("Callback called: %s", task_output)
        append_event(self.job_id, task_name + " has been finished")
        append_task_output(self.job_id, task_output.exported_output, task_name)

    def plan_itinerary(self, agent, city, travel_dates, interests):
        task_name = "plan_itinerary"
        return Task(
            description=dedent(
                f"""**Task**: Expand the city guide into a travel itinerary with detailed per-day plans, including weather forecasts, places to eat, packing suggestions, and a budget breakdown. You must suggest actual places to visit, actual hotels to stay, and actual restaurants to go to.
                **Parameters**: 1. City: {city} 2. Trip Date: {travel_dates} 3. Traveler Interests: {interests}"""
            ),
            agent=agent,
            expected_output=dedent("""Markdown"""),
            callback=lambda task_output: self.append_event_callback(
                task_name, task_output
            ),
        )

    def identify_city(self, agent, origin, cities, interests, travel_dates):
        task_name = "identify_city"
        return Task(
            description=dedent(
                f"""**Task**:  Analyze and select the best city for the trip based on specific criteria such as weather patterns, seasonal events, and travel costs. This task involves comparing multiple cities, considering factors like current weather conditions, upcoming cultural or seasonal events, and overall travel expenses. Your final answer must be a detailed report on the chosen city, including actual flight costs, weather forecast, and attractions.
                    **Parameters**: 1. Origin: {origin} 2. Cities: {cities} 3. Interests: {interests} 4. Travel Date: {travel_dates}"""
            ),
            agent=agent,
            expected_output=dedent("""Markdown"""),
            callback=lambda task_output: self.append_event_callback(
                task_name, task_output
            ),
        )

    def gather_city_info(self, agent, city, travel_dates, interests):
        task_name = "gather_city_info"
        return Task(
            description=dedent(
                f"""**Task**: Compile an in-depth guide for the selected city, gathering information about key attractions, local customs, special events, and daily activity recommendations. This guide should provide a thorough overview of what the city has to offer, including hidden gems, cultural hotspots, must-visit landmarks, weather forecasts, and high-level costs.
                    **Parameters**: 1. Cities: {city} 2. Interests: {interests} 3. Travel Date: {travel_dates}"""
            ),
            agent=agent,
            expected_output=dedent("""Markdown"""),
            callback=lambda task_output: self.append_event_callback(
                task_name, task_output
            ),
        )
