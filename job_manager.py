from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict
from threading import Lock
from utils.logging import logger
from typing import Any

jobs_lock = Lock()
jobs: Dict[str, "Job"] = {}


@dataclass
class Event:
    timestamp: datetime
    data: Any


@dataclass
class TaskOutput:
    timestamp: datetime
    data: Any
    task: str


@dataclass
class Job:
    status: str
    events: List[Event]
    result: str
    taskOutput: List[TaskOutput]


def append_event(job_id: str, event_data: Any):
    with jobs_lock:
        if job_id not in jobs:
            logger.info("Job %s started", job_id)
            jobs[job_id] = Job(status="STARTED", events=[], taskOutput=[], result="")
        else:
            logger.info("Appending event for job %s/ Data: %s", job_id, event_data)

        jobs[job_id].events.append(Event(timestamp=datetime.now(), data=event_data))


def append_task_output(job_id: str, event_data: Any, task_name: str):
    with jobs_lock:
        logger.info(
            "Appending task output for job %s/ Task: %s/ Data: %s",
            job_id,
            task_name,
            event_data,
        )
        jobs[job_id].taskOutput.append(
            TaskOutput(timestamp=datetime.now(), data=event_data, task=task_name)
        )
