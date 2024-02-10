from datetime import datetime
from enum import Enum
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, validator

from instruct_multilingual.schemas.task import Task3SubmissionResponseSchema, Task1SubmissionResponseSchema, \
    Task2SubmissionResponseSchema


class GenderOptions(str, Enum):
    male = "male"
    female = "female"
    non_binary = "non-binary"
    prefer_not_to_say = "prefer not to say"
    other = "other"


# schemas for creating a user
class UserRequestSchema(BaseModel):
    username: str
    image_url: str
    country_code: Optional[UUID]
    language_codes: Optional[List[UUID]]
    age_range: Optional[List[Optional[int]]]
    gender: Optional[GenderOptions]
    dialects: Optional[List[str]]

    @validator("age_range")
    def age_range_must_be_valid(cls, v):
        """
        Validates that the age range is valid and contains two values.
        """
        if v is not None:
            if len(v) < 2 or len(v) > 2:
                raise ValueError(
                    "age range must contain two values, lower bound and upper bound. "
                    "If there is no upper bound, use null. "
                    "If there is no lower bound, use null."
                )
            if v[0] is not None and v[0] < 0:
                raise ValueError("age range lower bound must be greater than or equal to 0")
            if v[1] is not None and v[1] < 0:
                raise ValueError("age range upper bound must be greater than or equal to 0")
            if v[0] is not None and v[1] is not None and v[0] > v[1]:
                raise ValueError("age range lower bound must be less than or equal to upper bound")

        return v
    
    @validator("dialects", each_item=True)
    def dialect_must_be_less_than_50_char(cls, v):
        """
        Validates that the dialect is less than or equal to 50 characters.
        Param each_item allows the validator to run on each item in the list.
        """
        if v is not None and len(v) > 50:
            raise ValueError("Dialect must be less than or equal to 50 characters.")
        return v


class UserResponseSchema(BaseModel):
    id: UUID
    username: str
    image_url: str
    country_code: Optional[UUID]
    language_codes: Optional[List[UUID]]
    age_range: Optional[List[Optional[int]]]
    gender: Optional[GenderOptions]
    dialects: Optional[List[str]]
    created_at: datetime

    @validator("age_range", pre=True)
    def convert_age_range_to_list(cls, v):
        """
        Converts the age range which is a postgres dialect NumericRange to a list.

        Runs before the standard validator.
        """
        if v is None:
            return v

        # by default, INT4RANGE uses a canonical form of '[)'
        # https://www.postgresql.org/docs/current/rangetypes.html
        # so let's work with that and subtract 1 from the upper bound
        # if it is not null, instead of creating our own custom range type.
        lower_bound = v.lower
        upper_bound = v.upper

        if upper_bound is not None:
            upper_bound = upper_bound - 1

        return [lower_bound, upper_bound]


# schemas for getting language and country options
# that are available to a user
class UserLanguageOptionsSchema(BaseModel):
    id: UUID
    code: str
    name: str
    character_code: str
    direction: str


class UserLanguageOptionsResponseSchema(BaseModel):
    options: List[UserLanguageOptionsSchema]


class UserCountryOptionsSchema(BaseModel):
    id: UUID
    code: str
    name: str


class UserCountryOptionsResponseSchema(BaseModel):
    options: List[UserCountryOptionsSchema]


class UserTaskContributionPaginationResponseSchema(BaseModel):
    total_count: int
    page: int
    page_size: int
    total_pages: int
    results: List[Union[
        Task1SubmissionResponseSchema,
        Task2SubmissionResponseSchema,
        Task3SubmissionResponseSchema
    ]
]
