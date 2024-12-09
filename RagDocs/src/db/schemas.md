# Python File Documentation

This document outlines the structure and functionality of a Python file containing various Pydantic models for data representation and handling.  The file leverages several external libraries including `datetime`, `typing`, `pydantic`, `bson`, and custom enums.

## Imports

```python
from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from bson import ObjectId
from src.enums import CallTypes, Dialers, ProfileTypes, UserRoles
from pydantic_core import core_schema
```

## Custom Type: `PyObjectId`

This class extends the `str` type to handle MongoDB ObjectIds. It ensures proper validation and serialization.

```python
class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        # ... (Schema definition for handling ObjectId serialization and validation) ...
    @classmethod
    def validate(cls, value) -> ObjectId:
        # ... (Validation logic to ensure a valid ObjectId) ...
```

## Models

### Transcripts

*   **`TranscriptTurns`**: Represents a single turn in a transcript.
    ```python
    class TranscriptTurns(BaseModel):
        transcript: str | None = None
        speaker: str | None = None
        start_time: float | None = None
        end_time: float | None = None
    ```
*   **`TranscriptResponse`**:  Represents a complete transcript.
    ```python
    class TranscriptResponse(BaseModel):
        _id: PyObjectId
        turns: list[TranscriptTurns] | None = None
        createdAt: datetime | None = None
        updatedAt: datetime | None = None
    ```

### Summaries

*   **`Summary`**: Contains a summary of a call.
    ```python
    class Summary(BaseModel):
        callSummary: str | None = None
        strengths: list[str] | None = None
        areasToImprove: list[str] | None = None
        skillRating: dict | None = None
        overallRating: float | None = None
    ```
*   **`SummariesResponse`**:  Represents a complete summary response.
    ```python
    class SummariesResponse(BaseModel):
        _id: PyObjectId
        summary: Summary | None = None
        createdAt: datetime | None = None
        updatedAt: datetime | None = None
    ```

### Live Insights

*   **`LiveInsight`**: Represents a single live insight during a call.
    ```python
    class LiveInsight(BaseModel):
        nudge: str | None = None
        time: float | None = None
        turn_id: int | None = None
    ```
*   **`LiveInsightsResponse`**: Represents a collection of live insights.
    ```python
    class LiveInsightsResponse(BaseModel):
        _id: PyObjectId
        conversation: str
        insights: list[LiveInsight] | None = None
        createdAt: datetime | None = None
        updatedAt: datetime | None = None
    ```

### Users

```python
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
```

### Personas

*   **`Persona`**: Represents a call persona.
    ```python
    class Persona(BaseModel):
        id: PyObjectId | None = Field(default=None, alias="_id")
        personaName: str
        callScenario: str
        difficultyLevel: str
        userId: PyObjectId | None = None
        linkedInUrl: str
        model_config = ConfigDict(populate_by_name=True)
    ```
*   **`PersonasResponse`**: Represents a persona response, including timestamps.
    ```python
    class PersonasResponse(BaseModel):
        id: PyObjectId = Field(..., validation_alias="_id")
        personaName: str
        callScenario: str
        difficultyLevel: str
        userId: PyObjectId | None = None
        linkedInUrl: str
        createdAt: datetime | None = None
        updatedAt: datetime | None = None
        model_config = ConfigDict(populate_by_name=True)
    ```

### Profile Information

*   **`LinkedInInfo`**: Contains information extracted from LinkedIn.
*   **`ProductInfo`**: Contains information about a product.
*   **`HubspotInfo`**: Contains information from Hubspot.
*   **`ProfileInfo`**:  Combines information from various sources.
*   **`ProfileInfoResponse`**: Response model for profile information, includes timestamps.


### Conversations

*   **`Conversation`**: Represents a single conversation.
    ```python
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
        model_config = ConfigDict(populate_by_name=True)
    ```
*   **`ConversationsResponse`**: Represents a conversation response, including timestamps.
*   **`PageParams`**:  Pagination parameters for list responses.
*   **`ConversationsListResponse`**:  Response for a list of conversations.


### Prompts

*   **`PromptCreationInput`**: Input for creating a prompt.
*   **`PromptUpdateInput`**: Input for updating a prompt.
*   **`PromptResponse`**: Response for a prompt, including timestamps.


This markdown provides a comprehensive overview of the Python file's contents.  Each model's fields and their types are clearly documented, allowing for easy understanding of the data structures used.  The use of `ConfigDict` for `populate_by_name` is also highlighted.
