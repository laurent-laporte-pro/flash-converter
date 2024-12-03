from celery.result import AsyncResult
from pydantic import BaseModel

from flash_converter.tasks import Payload


class Task(BaseModel):
    task_id: str
    task_name: str
    state: str = "PENDING"

    @classmethod
    def from_job(cls, job: AsyncResult) -> "Task":
        payload = Payload(*job.get())
        return cls(task_id=job.id, task_name=payload.filename, state=job.state)


class TaskList(BaseModel):
    tasks: list[Task]
    total: int
    page: int
    limit: int
