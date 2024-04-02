from crewai import Task, Agent
from textwrap import dedent
from job_manager import append_task_output, append_event
from utils.logging import logger
import markdown
import json

"""
Creating Tasks Cheat Sheet:
- Begin with the end in mind. Identify the specific outcome your tasks are aiming to achieve.
- Break down the outcome into actionable tasks, assigning each task to the appropriate agent.
- Ensure tasks are descriptive, providing clear instructions and expected deliverables.

Goal:
- Develop a detailed itinerary, including city selection, attractions, and practical travel advice.

Key Steps for Task Creation:
1. Identify the Desired Outcome: Define what success looks like for your project.
    - A detailed 7 day travel itenerary.

2. Task Breakdown: Divide the goal into smaller, manageable tasks that agents can execute.
    - Itenerary Planning: develop a detailed plan for each day of the trip.
    - City Selection: Analayze and pick the best cities to visit.
    - Local Tour Guide: Find a local expert to provide insights and recommendations.

3. Assign Tasks to Agents: Match tasks with agents based on their roles and expertise.

4. Task Description Template:
  - Use this template as a guide to define each task in your CrewAI application. 
  - This template helps ensure that each task is clearly defined, actionable, and aligned with the specific goals of your project.

  Template:
  ---------
  def [task_name](self, agent, [parameters]):
      return Task(description=dedent(f'''
      **Task**: [Provide a concise name or summary of the task.]
      **Description**: [Detailed description of what the agent is expected to do, including actionable steps and expected outcomes. This should be clear and direct, outlining the specific actions required to complete the task.]

      **Parameters**: 
      - [Parameter 1]: [Description]
      - [Parameter 2]: [Description]
      ... [Add more parameters as needed.]

      **Note**: [Optional section for incentives or encouragement for high-quality work. This can include tips, additional context, or motivations to encourage agents to deliver their best work.]

      '''), agent=agent)

"""


class TravelTasks:
    def __init__(self, job_id):
        self.job_id = job_id

    def append_event_callback(self, task_name, task_output):
        logger.info("Callback called: %s", task_output)
        append_event(self.job_id, task_output.exported_output)
        append_task_output(self.job_id, task_output.exported_output, task_name)

    def plan_itinerary(self, agent, city, travel_dates, interests):
        task_name = "plan_itinerary"
        return Task(
            description=dedent(
                f"""
            **Task**: Develop a Travel Itinerary
            **Description**: Expand the city guide into a travel itinerary with detailed 
                per-day plans, including weather forecasts, places to eat, packing suggestions, 
                and a budget breakdown. You MUST suggest actual places to visit, actual hotels to stay, 
                and actual restaurants to go to. This itinerary should cover all aspects of the trip, 
                from arrival to departure, integrating the city guide information with practical travel logistics.

            **Parameters**: 
            - City: {city}
            - Trip Date: {travel_dates}
            - Traveler Interests: {interests}
        """
            ),
            agent=agent,
            expected_output=dedent("""Text"""),
            callback=lambda task_output: self.append_event_callback(
                task_name, task_output
            ),
        )

    def identify_city(self, agent, origin, cities, interests, travel_dates):
        task_name = "identify_city"
        return Task(
            description=dedent(
                f"""
                    **Task**:  Identify the Best City for the Trip
                    **Description**: Analyze and select the best city for the trip based on specific 
                        criteria such as weather patterns, seasonal events, and travel costs. 
                        This task involves comparing multiple cities, considering factors like current weather 
                        conditions, upcoming cultural or seasonal events, and overall travel expenses. 
                        Your final answer must be a detailed report on the chosen city, 
                        including actual flight costs, weather forecast, and attractions.


                    **Parameters**: 
                    - Origin: {origin}
                    - Cities: {cities}
                    - Interests: {interests}
                    - Travel Date: {travel_dates}
                """
            ),
            agent=agent,
            expected_output=dedent("""Text"""),
            callback=lambda task_output: self.append_event_callback(
                task_name, task_output
            ),
        )

    def gather_city_info(self, agent, city, travel_dates, interests):
        task_name = "gather_city_info"
        return Task(
            description=dedent(
                f"""
                    **Task**:  Gather In-depth City Guide Information
                    **Description**: Compile an in-depth guide for the selected city, gathering information about 
                        key attractions, local customs, special events, and daily activity recommendations. 
                        This guide should provide a thorough overview of what the city has to offer, including 
                        hidden gems, cultural hotspots, must-visit landmarks, weather forecasts, and high-level costs.

                    **Parameters**: 
                    - Cities: {city}
                    - Interests: {interests}
                    - Travel Date: {travel_dates}
                """
            ),
            agent=agent,
            expected_output=dedent("""Text"""),
            callback=lambda task_output: self.append_event_callback(
                task_name, task_output
            ),
        )
