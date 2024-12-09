from pydantic import BaseModel
from typing import Union, List
from enum import Enum


class ChartType(str, Enum):
    DURATION = "duration"
    PIE = "pie"
    METER = "meter"
    BAR = "bar"
    TEXT = "text"


class PostCallAnalyticsRequest(BaseModel):
    reportee: str
    timeline: str


class AnalyticsRoleplayDuration(BaseModel):
    heading: str = "Roleplay Duration"
    type: ChartType = ChartType.DURATION
    data: dict


class AnalyticsRoleplayTypes(BaseModel):
    heading: str = "Roleplay Types"
    type: ChartType = ChartType.PIE
    data: dict


class AnalyticsSalesCallOutcomes(BaseModel):
    heading: str = "Sales call Outcomes"
    type: ChartType = ChartType.PIE
    data: dict


class AnalyticsOverallCallPerformanceTeam(BaseModel):
    heading: str = "Overall Call Performance"
    type: ChartType = ChartType.BAR
    data: dict


class AnalyticsOverallCallPerformanceUser(BaseModel):
    heading: str = "Overall Call Performance"
    type: ChartType = ChartType.METER
    data: dict


class AnalyticsOverallCallStagePerformance(BaseModel):
    heading: str = "Overall Call Stage Performance"
    type: ChartType = ChartType.BAR
    data: dict


class AnalyticsMostCommonObjection(BaseModel):
    heading: str = "Most Common Objection"
    type: ChartType = ChartType.TEXT
    data: dict


class AnalyticsMostCommonObjectionResponse(BaseModel):
    heading: str = "Response for Most Common Objection"
    type: ChartType = ChartType.TEXT
    data: dict


class AnalyticsExpertAttributes(BaseModel):
    heading: str = "Expert Attributes"
    type: ChartType = ChartType.TEXT
    data: dict


class AnalyticsStruggleAttributes(BaseModel):
    heading: str = "Struggle Attributes"
    type: ChartType = ChartType.TEXT
    data: dict


class AnalyticsSuggestionsForImprovement(BaseModel):
    heading: str = "Suggestions for Improvement"
    type: ChartType = ChartType.TEXT
    data: dict


class PostCallAnalyticsResponse(BaseModel):
    userId: str
    role: str
    reportee: str
    timeline: str
    analyticsReport: List[
        Union[
            AnalyticsRoleplayDuration,
            AnalyticsRoleplayTypes,
            AnalyticsSalesCallOutcomes,
            AnalyticsOverallCallPerformanceTeam,
            AnalyticsOverallCallPerformanceUser,
            AnalyticsOverallCallStagePerformance,
            AnalyticsMostCommonObjection,
            AnalyticsMostCommonObjectionResponse,
            AnalyticsExpertAttributes,
            AnalyticsStruggleAttributes,
            AnalyticsSuggestionsForImprovement,
        ]
    ]
