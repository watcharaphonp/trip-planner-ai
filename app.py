# Standard library imports
from datetime import datetime
import json
from threading import Thread
from uuid import uuid4

# Related third-party imports
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from dotenv import load_dotenv

# Local application/library specific imports
from crew import TripCrew
from job_manager import append_event, jobs, jobs_lock, Event
from utils.logging import logger


load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


def kickoff_crew(job_id, user_id, session_id, origin, cities, date_range, interests):
    logger.info(f"Crew for job {job_id} is starting")

    crew_response = None
    try:
        trip_planner_crew = TripCrew(job_id, user_id, session_id)
        trip_planner_crew.setup_crew(origin, cities, date_range, interests)
        crew_response = trip_planner_crew.kickoff()
        logger.info(f"Crew for job {job_id} is complete", crew_response.data)
        # Handle the error as needed

    except Exception as e:
        logger.error(f"Error in kickoff_crew for job {job_id}: {e}")
        append_event(job_id, f"An error occurred: {e}")
        # Handle other exceptions

    with jobs_lock:
        if job_id in jobs:
            jobs[job_id].status = "COMPLETE"
            jobs[job_id].result = crew_response.data
            jobs[job_id].metrics = crew_response.metrics
            jobs[job_id].events.append(
                Event(timestamp=datetime.now(), data="Crew complete")
            )


@app.route("/api/crew", methods=["POST"])
def run_crew():
    logger.info("Received request to run crew")
    # Validation
    data = request.json
    if (
        not data
        or "user_id" not in data
        or "origin" not in data
        or "cities" not in data
        or "date_range" not in data
        or "interests" not in data
    ):
        abort(400, description="Invalid input data provided.")

    job_id = str(uuid4())
    user_id = str(data["user_id"])
    session_id = str(data["session_id"])
    origin = data["origin"]
    cities = data["cities"]
    date_range = data["date_range"]
    interests = data["interests"]

    thread = Thread(
        target=kickoff_crew,
        args=(job_id, user_id, session_id, origin, cities, date_range, interests),
    )
    thread.start()

    return jsonify({"job_id": job_id, "user_id": user_id}), 202


@app.route("/api/crew/<job_id>", methods=["GET"])
def get_status(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
        if job is None:
            abort(404, description="Job not found")

    # Parse the job.result string into a JSON object
    try:
        result_json = json.loads(job.result)
    except json.JSONDecodeError:
        # If parsing fails, set result_json to the original job.result string
        result_json = job.result

    return jsonify(
        {
            "job_id": job_id,
            "status": job.status,
            "result": result_json,
            "metrics": job.metrics,
            "events": [
                {"timestamp": event.timestamp.isoformat(), "data": event.data}
                for event in job.events
            ],
            "task_output": [
                {
                    "timestamp": taskOutput.timestamp.isoformat(),
                    "data": taskOutput.data,
                    "task": taskOutput.task,
                }
                for taskOutput in job.taskOutput
            ],
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=3001)
