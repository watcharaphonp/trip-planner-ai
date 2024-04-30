from datetime import datetime
from typing import Callable
from agents import TravelAgents
from job_manager import append_event
from tasks import TravelTasks
from crewai import Crew, Process


class CrewResponse:
    def __init__(self, data: str, metrics: dict | None):
        self.data = data
        self.metrics = metrics


class TripCrew:
    def __init__(self, job_id: str, user_id: str, session_id: str):
        self.job_id = job_id
        self.user_id = user_id
        self.session_id = session_id
        self.crew = None

    def setup_crew(self, origin, cities, date_range, interests):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = TravelAgents(user_id=self.user_id, session_id=self.session_id)
        tasks = TravelTasks(job_id=self.job_id)

        # Define your custom agents and tasks here
        city_selector_agent = agents.city_selection_agent()
        local_expert_agent = agents.local_expert()
        travel_concierge_agent = agents.travel_concierge()

        identify_task = tasks.identify_task(
            city_selector_agent, origin, cities, interests, date_range
        )
        gather_task = tasks.gather_task(
            local_expert_agent, origin, cities, interests, date_range
        )
        plan_task = tasks.plan_task(
            travel_concierge_agent, origin, cities, interests, date_range
        )

        self.crew = Crew(
            agents=[city_selector_agent, local_expert_agent, travel_concierge_agent],
            tasks=[identify_task, gather_task, plan_task],
            verbose=True,
        )

    def kickoff(self):
        if not self.crew:
            append_event(self.job_id, "Crew not set up")
            return CrewResponse("Crew not set up", None)

        append_event(self.job_id, "Task Started")
        try:
            results = self.crew.kickoff()
            append_event(self.job_id, "Task Complete")
            return CrewResponse(results, self.crew.usage_metrics)
        except Exception as e:
            append_event(self.job_id, f"An error occurred: {e}")
            return CrewResponse(str(e), None)
