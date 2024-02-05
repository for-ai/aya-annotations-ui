from typing import List, Optional, Union

from pydantic import BaseModel, validator

class LeaderboardBaseRecord(BaseModel):
    username: str
    languages: Optional[List[str]]
    image_url: str
    rank: int
    points: int


class LeaderboardDailyRecord(LeaderboardBaseRecord):
    day: str


class LeaderboardWeeklyRecord(LeaderboardBaseRecord):
    week_of: str


class LeaderboardByLanguageRecord(LeaderboardBaseRecord):
    language: str
    blended_rank: int
    blended_points: int
    quality_score: Optional[float]

    class Config:
        exclude = {"languages"}

    @validator('quality_score')
    def result_check(cls, v):
        if v is not None:
            return round(v, 4)

class LeaderboardOverallRecord(LeaderboardBaseRecord):
    blended_rank: int
    blended_points: int
    quality_score: Optional[float]

    @validator('quality_score')
    def result_check(cls, v):
        if v is not None:
            return round(v, 4)

class LeaderboardRecordList(BaseModel):
    records: List[Union[
        LeaderboardOverallRecord,
        LeaderboardDailyRecord, 
        LeaderboardWeeklyRecord, 
        LeaderboardByLanguageRecord,
        LeaderboardBaseRecord,
    ]]

    current_user: Optional[LeaderboardBaseRecord]
    total_count: Optional[int]


class OverallLeaderboardRecordList(BaseModel):
    records: List[LeaderboardOverallRecord]

    current_user: Optional[LeaderboardOverallRecord]
    total_count: int

class LanguageLeaderboardRecordList(BaseModel):
    records: List[LeaderboardByLanguageRecord]
    current_user: Optional[LeaderboardByLanguageRecord]