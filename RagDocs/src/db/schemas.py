from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from bson import ObjectId
from src.enums import CallTypes, Dialers, ProfileTypes, UserRoles
from pydantic_core import core_schema


class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    core_schema.chain_schema(
                        [
                            core_schema.str_schema(),
                            core_schema.no_info_plain_validator_function(cls.validate),
                        ]
                    ),
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, value) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")

        return ObjectId(value)


# Transcripts
class TranscriptTurns(BaseModel):
    transcript: str | None = None
    speaker: str | None = None
    start_time: float | None = None
    end_time: float | None = None


class TranscriptResponse(BaseModel):
    _id: PyObjectId
    turns: list[TranscriptTurns] | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


# Summaries
class Summary(BaseModel):
    callSummary: str | None = None
    strengths: list[str] | None = None
    areasToImprove: list[str] | None = None
    skillRating: dict | None = None
    overallRating: float | None = None


class SummariesResponse(BaseModel):
    _id: PyObjectId
    summary: Summary | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


# Live Insights
class LiveInsight(BaseModel):
    nudge: str | None = None
    time: float | None = None
    turn_id: int | None = None


class LiveInsightsResponse(BaseModel):
    _id: PyObjectId
    conversation: str
    insights: list[LiveInsight] | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


# Users
class User(BaseModel):
    id: PyObjectId
    name: str
    email: EmailStr
    dialers: list | None = None
    isVerified: bool | None = None
    isActive: bool | None = None
    managers: list | None = None
    subordinates: list | None = None
    roles: UserRoles | None = None
    companyUrl: str | None = None


# Personas
class Persona(BaseModel):
    id: PyObjectId | None = Field(default=None, alias="_id")
    personaName: str
    callScenario: str
    difficultyLevel: str
    userId: PyObjectId | None = None
    linkedInUrl: str

    model_config = ConfigDict(
        populate_by_name=True,
    )


class PersonasResponse(BaseModel):
    id: PyObjectId = Field(..., validation_alias="_id")
    personaName: str
    callScenario: str
    difficultyLevel: str
    userId: PyObjectId | None = None
    linkedInUrl: str
    createdAt: datetime | None = None
    updatedAt: datetime | None = None

    model_config = ConfigDict(
        populate_by_name=True,
    )


class LinkedInInfo(BaseModel):
    url: str
    data: dict
    summary: str
    buyingStyle: str


class ProductInfo(BaseModel):
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    url: str
    data: dict
    summary: str

class HubspotInfo(BaseModel):
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    email: str | None = None
    email_chain: str | None = None
    hs_linkedin_url: str | None = None
    hs_object_id: str | None = None
    notes: str | None = None

class ProfileInfo(BaseModel):
    id: PyObjectId = Field(..., alias="_id")
    profileType: ProfileTypes
    profileId: PyObjectId
    productInfo: ProductInfo | None = None
    hubspotInfo: HubspotInfo | None = None
    linkedinInfo: LinkedInInfo | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None

    model_config = ConfigDict(
        populate_by_name=True,
    )


class ProfileInfoResponse(BaseModel):
    id: PyObjectId = Field(..., validation_alias="_id")
    profileType: ProfileTypes
    profileId: PyObjectId
    productInfo: ProductInfo
    linkedinInfo: LinkedInInfo
    hubspotInfo: HubspotInfo
    createdAt: datetime | None = None
    updatedAt: datetime | None = None

    model_config = ConfigDict(
        populate_by_name=True,
    )


# Conversations
class Conversation(BaseModel):
    conversationId: str = Field(..., validation_alias="_id")
    userId: PyObjectId
    dialer: Dialers | None = None
    callType: CallTypes | None = None
    callScenario: str | None = None
    callRecordingUrl: str | None = None
    callDuration: str | None = None
    callDateTime: datetime | None = None
    persona: Persona | PyObjectId | None = None
    profileInfo: ProfileInfo | PyObjectId | None = None
    metadata: dict | None = None

    model_config = ConfigDict(
        populate_by_name=True,
    )


class ConversationsResponse(BaseModel):
    conversationId: str = Field(..., validation_alias="_id")
    userId: PyObjectId
    dialer: Dialers | None = None
    callType: CallTypes | None = None
    callScenario: str | None = None
    callRecordingUrl: str | None = None
    callDuration: str | None = None
    callDateTime: datetime | None = None
    persona: Persona | PyObjectId | None = None
    profileInfo: ProfileInfo | PyObjectId | None = None
    metadata: dict | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    model_config = ConfigDict(
        populate_by_name=True,
    )


class PageParams(BaseModel):
    totalItems: int
    totalPages: int
    page: int
    size: int


class ConversationsListResponse(BaseModel):
    conversations: list[ConversationsResponse]
    pageParam: PageParams


class PromptCreationInput(BaseModel):
    promptType: str
    callType: CallTypes
    callScenario: str | None = "default"
    difficultyLevel: str | None = "default"
    body: str
    modelSettings: dict | None = None


class PromptUpdateInput(BaseModel):
    body: str | None = None
    modelSettings: dict | None = None


class PromptResponse(BaseModel):
    id: PyObjectId = Field(..., validation_alias="_id")
    name: str
    body: str
    modelSettings: dict | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None

    model_config = ConfigDict(
        populate_by_name=True,
    )
