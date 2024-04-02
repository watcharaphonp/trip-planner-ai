from datetime import datetime
from typing import Callable
from agents import TravelAgents
from job_manager import append_event
from tasks import TravelTasks
from crewai import Crew, Process


class TripCrew:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.crew = None

    def setup_crew(self, origin, cities, date_range, interests):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = TravelAgents()
        tasks = TravelTasks(job_id=self.job_id)

        # Define your custom agents and tasks here
        expert_travel_agent = agents.expert_travel_agent()
        city_selection_expert = agents.city_selection_expert()
        local_tour_guide = agents.local_tour_guide()

        identify_city = tasks.identify_city(
            city_selection_expert, origin, cities, interests, date_range
        )

        gather_city_info = tasks.gather_city_info(
            local_tour_guide, cities, date_range, interests
        )

        plan_itinerary = tasks.plan_itinerary(
            expert_travel_agent, cities, date_range, interests
        )

        self.crew = Crew(
            agents=[expert_travel_agent, city_selection_expert, local_tour_guide],
            tasks=[plan_itinerary, identify_city, gather_city_info],
            verbose=True,
            process=Process.sequential,
        )

    def kickoff(self):
        if not self.crew:
            append_event(self.job_id, "Crew not set up")
            return "Crew not set up"

        append_event(self.job_id, "Task Started")
        try:
            results = self.crew.kickoff()
            append_event(self.job_id, "Task Complete")
            return str(results)
        except Exception as e:
            append_event(self.job_id, f"An error occurred: {e}")
            return str(e)
