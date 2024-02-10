from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, validator


class TaskSchema(BaseModel):
    id: UUID
    prompt: str
    completion: str
    is_contributed: bool


class TaskListSchema(BaseModel):
    tasks: List[TaskSchema]


class TaskAuditRequestSchema(BaseModel):
    task_id: UUID
    submitted_by: UUID
    submitted_prompt: str
    submitted_completion: str
    prompt_edited: bool
    completion_edited: bool
    prompt_rating: Optional[int] = None
    completion_rating: Optional[int] = None


class TaskAuditResponseSchema(TaskAuditRequestSchema):
    id: UUID
    created_at: datetime


class TaskContributionRequestSchema(BaseModel):
    submitted_by: UUID
    submitted_prompt: str
    submitted_completion: str
    language_id: UUID

    # if the submitted prompt and completion are empty, raise a validation error
    @validator("submitted_prompt")
    def prompt_must_be_nonempty(cls, v):
        if not v:
            raise ValueError("prompt must not be empty")

        return v

    @validator("submitted_completion")
    def completion_must_be_nonempty(cls, v):
        if not v:
            raise ValueError("completion must not be empty")

        return v


class TaskContributionResponseSchema(TaskContributionRequestSchema):
    id: UUID
    created_at: datetime


class TaskContributionAuditRequestSchema(BaseModel):
    task_contribution_id: UUID
    submitted_by: UUID
    submitted_prompt: str
    submitted_completion: str
    prompt_edited: bool
    completion_edited: bool
    prompt_rating: Optional[int] = None
    completion_rating: Optional[int] = None


class TaskContributionAuditResponseSchema(TaskContributionAuditRequestSchema):
    id: UUID
    created_at: datetime


class TaskAuditReviewRequestSchema(BaseModel):
    task_audit_id: UUID
    submitted_by: UUID
    edited_prompt_rating: int
    edited_completion_rating: int
    improved_edited_prompt: Optional[str] = None
    improved_edited_completion: Optional[str] = None
    feedback: Optional[str] = None


class TaskAuditReviewResponseSchema(TaskAuditReviewRequestSchema):
    id: UUID
    created_at: datetime


class TaskContributionAuditReviewRequestSchema(BaseModel):
    task_contribution_audit_id: UUID
    submitted_by: UUID
    edited_prompt_rating: int
    edited_completion_rating: int
    improved_edited_prompt: Optional[str] = None
    improved_edited_completion: Optional[str] = None
    feedback: Optional[str] = None


class TaskContributionAuditReviewResponseSchema(TaskContributionAuditReviewRequestSchema):
    id: UUID
    created_at: datetime


class TaskAuditGetResponseSchema(BaseModel):
    id: UUID
    contributed_by_id: UUID
    contributed_by: str
    contributed_by_image: str
    original_prompt: str
    original_completion: str
    edited_prompt: str
    edited_completion: str
    is_contributed: bool


class TaskAuditGetResponseListSchema(BaseModel):
    task_audits: List[TaskAuditGetResponseSchema]


class Task1SubmissionResponseSchema(BaseModel):
    id: UUID
    submitted_by: UUID
    submitted_prompt: str
    submitted_completion: str
    prompt_edited: bool
    completion_edited: bool
    prompt_rating: Optional[int] = None
    completion_rating: Optional[int] = None
    created_at: datetime
    edit_distance: Optional[float] = None


class Task2SubmissionResponseSchema(BaseModel):
    id: UUID
    submitted_by: UUID
    submitted_prompt: str
    submitted_completion: str
    language_id: UUID
    created_at: datetime


class Task3SubmissionResponseSchema(BaseModel):
    id: UUID
    original_prompt: str
    original_completion: str
    edited_prompt: str
    edited_completion: str
    edited_prompt_rating: int
    edited_completion_rating: int
    improved_prompt: Optional[str] = None
    improved_completion: Optional[str] = None
    improvement_feedback: str
    submitted_by: UUID
    created_at: datetime
