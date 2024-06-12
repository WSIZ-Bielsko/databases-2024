from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class JobRequest(BaseModel):
    id: UUID
    repo_url: str
    commit: str
    image_tag: str
    entry_point_file: str
    env_file_content: str
    cpu: float
    ram_mb: float
    priority: int
    user_id: UUID
    submitted_at: datetime | None
    cancelled_at: datetime | None


class VolumeClaim(BaseModel):
    id: UUID
    volume_id: UUID
    job_request_id: UUID
    mount_type: str


class Job(BaseModel):
    id: UUID
    request_id: UUID
    node_id: UUID
    started_at: datetime
    canceled_at: datetime | None
    finished_at: datetime | None


class Volume(BaseModel):
    id: UUID
    name: str


class Log(BaseModel):
    id: UUID
    job_id: UUID
    timestamp: datetime
    stream: str  # stdout or stderr
    level: str
    message: str


class User(BaseModel):
    id: UUID
    name: str


class Node(BaseModel):
    id: UUID
    name: str
    max_cpu: float
    max_ram: float


class NodeState(BaseModel):
    id: UUID
    node_id: UUID
    reported_at: datetime
    used_cpu: float
    used_ram: float
