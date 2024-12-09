# MongoDB Models Documentation

This document describes the MongoDB models used in the application.  These models utilize the `mongoengine` library for object-document mapping.

## Imports

```python
from datetime import datetime
from mongoengine import (
    EnumField,
    Document,
    EmbeddedDocument,
    StringField,
    IntField,
    ListField,
    DateTimeField,
    DynamicDocument,
    DictField,
    URLField,
    ReferenceField,
    EmbeddedDocumentField,
)
from mongoengine.base.fields import ObjectIdField
from mongoengine.queryset.queryset import QuerySet
from ..enums import *
from bson import json_util
```

## Custom QuerySet

```python
class FullDocumentQuerySet(QuerySet):
    def full(self):
        """
        Retrieves all documents in the queryset, populating referenced documents.

        Returns:
            list: A list of dictionaries representing the documents, with referenced documents fully populated.  
                  WARNING: DO NOT USE OUTPUT OF THIS FOR REFERENCE FIELDS.
        """
        return [doc.full() for doc in self]
```

## Models

### Personas

```python
class Personas(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    personaName = StringField(required=True, max_length=100)
    callScenario = StringField(required=True)
    difficultyLevel = StringField(required=True)
    userId = ObjectIdField(required=True)
    linkedInUrl = StringField(required=True)
```

Represents a persona used in conversations.

* `createdAt`: DateTime - Timestamp of creation.
* `updatedAt`: DateTime - Timestamp of last update.
* `personaName`: String (required, max 100 characters) - Name of the persona.
* `callScenario`: String (required) - Scenario for the persona.
* `difficultyLevel`: String (required) - Difficulty level of the persona.
* `userId`: ObjectId (required) - ID of the user associated with the persona.
* `linkedInUrl`: String (required) - LinkedIn URL for the persona.


### Integrations

```python
class Integrations(DynamicDocument):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    service = StringField(required=True)
    data = DictField()
    userId = ObjectIdField(required=True)
```

Represents an integration with an external service.  Uses `DynamicDocument` allowing for flexible schema.

* `createdAt`: DateTime - Timestamp of creation.
* `updatedAt`: DateTime - Timestamp of last update.
* `service`: String (required) - Name of the integrated service.
* `data`: Dict -  Arbitrary data related to the integration.
* `userId`: ObjectId (required) - ID of the user associated with the integration.


### ProductInfos (Embedded Document)

```python
class ProductInfos(EmbeddedDocument):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    url = URLField(required=True)
    data = DictField(required=True)
    summary = StringField(required=True)
```

Embedded document containing product information.

* `createdAt`: DateTime - Timestamp of creation.
* `updatedAt`: DateTime - Timestamp of last update.
* `url`: URL (required) - URL of the product.
* `data`: Dict (required) -  Product data.
* `summary`: String (required) - Summary of the product.


### HubspotInfos (Embedded Document)

```python
class HubspotInfos(EmbeddedDocument):
    createdate = DateTimeField(default=datetime.now)
    lastmodifieddate = DateTimeField(default=datetime.now)
    email = StringField(required=True)
    email_chain = StringField(required=False)
    hs_linkedin_url = URLField(required=False)
    hs_object_id = StringField(required=True)
    notes = StringField(required=False)
```

Embedded document containing HubSpot information.

* `createdate`: DateTime - Creation date from HubSpot.
* `lastmodifieddate`: DateTime - Last modification date from HubSpot.
* `email`: String (required) - Email address.
* `email_chain`: String - Email chain.
* `hs_linkedin_url`: URL - LinkedIn URL from HubSpot.
* `hs_object_id`: String (required) - HubSpot object ID.
* `notes`: String - Notes.


### LinkedInInfos (Embedded Document)

```python
class LinkedInInfos(EmbeddedDocument):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    url = URLField(required=True)
    data = DictField(required=True)
    summary = StringField(required=True)
    buyingStyle = StringField(required=True)
```

Embedded document containing LinkedIn information.

* `createdAt`: DateTime - Timestamp of creation.
* `updatedAt`: DateTime - Timestamp of last update.
* `url`: URL (required) - LinkedIn URL.
* `data`: Dict (required) - LinkedIn data.
* `summary`: String (required) - Summary of LinkedIn profile.
* `buyingStyle`: String (required) - Buying style.


### ProfileInfos

```python
class ProfileInfos(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    profileType = EnumField(ProfileTypes, required=True)
    profileId = StringField(required=True)
    hubspotInfo = EmbeddedDocumentField(HubspotInfos)
    productInfo = EmbeddedDocumentField(ProductInfos)
    linkedinInfo = EmbeddedDocumentField(LinkedInInfos)
```

Represents profile information.

* `createdAt`: DateTime - Timestamp of creation.
* `updatedAt`: DateTime - Timestamp of last update.
* `profileType`: EnumField (required) - Type of profile.
* `profileId`: String (required) - ID of the profile.
* `hubspotInfo`: EmbeddedDocumentField - HubSpot information.
* `productInfo`: EmbeddedDocumentField - Product information.
* `linkedinInfo`: EmbeddedDocumentField - LinkedIn information.


### Conversations

```python
class Conversations(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    conversationId = StringField(required=True, primary_key=True)
    userId = ObjectIdField(required=True)
    dialer = EnumField(Dialers)
    callType = EnumField(CallTypes)
    callScenario = StringField()
    callRecordingUrl = URLField()
    callDuration = StringField()
    callDateTime = DateTimeField(default=datetime.now)
    persona = ReferenceField(Personas)
    metadata = DictField()
    profileInfo = ReferenceField(ProfileInfos)

    meta = {"queryset_class": FullDocumentQuerySet}

    def full(self):
        """
        WARNING: DO NOT USE OUTPUT OF THIS FOR REFERENCE FIELDS.
        """
        data = self.to_mongo(use_db_field=False)
        if self.persona:
            data["persona"] = self.persona.to_mongo(use_db_field=False)
        if self.profileInfo:
            data["profileInfo"] = self.profileInfo.to_mongo(use_db_field=False)
        return Conversations(**json_util.loads(json_util.dumps(data)))
```

Represents a conversation.

* `createdAt`: DateTime - Timestamp of creation.
* `updatedAt`: DateTime - Timestamp of last update.
* `conversationId`: String (required, primary key) - Unique ID of the conversation.
* `userId`: ObjectId (required) - ID of the user associated with the conversation.
* `dialer`: EnumField - Dialer used.
* `callType`: EnumField - Type of call.
* `callScenario`: String - Scenario of the call.
* `callRecordingUrl`: URL - URL of the call recording.
* `callDuration`: String - Duration of the call.
* `callDateTime`: DateTime - Timestamp of the call.
* `persona`: ReferenceField - Persona used in the conversation.
* `metadata`: Dict -  Additional metadata.
* `profileInfo`: ReferenceField - Profile information related to the conversation.


### Transcripts

```python
class Transcripts(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    conversationId = StringField(required=True, primary_key=True)
    turns = ListField(DictField(), default=list)
```

Represents a transcript of a conversation.

* `createdAt`: DateTime - Timestamp of creation.
* `updatedAt`: DateTime - Timestamp of last update.
* `conversationId`: String (required, primary key) - ID of the associated conversation.
* `turns`: ListField - List of turns in the conversation.


### LiveInsights

```python
class LiveInsights(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    conversationId = StringField(required=True, primary_key=True)
    insights = ListField(DictField(), default=list)
```

Represents live insights from a conversation.

* `createdAt`: DateTime - Timestamp of creation.
* `updatedAt`: DateTime - Timestamp of last update.
* `conversationId`: String (required, primary key) - ID of the associated conversation.
* `insights`: ListField - List of insights.


### Summaries

```python
class Summaries(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    conversationId = StringField(required=True, primary_key=True)
    summary = DictField()
```

Represents a summary of a conversation.

* `createdAt`: DateTime - Timestamp of creation.
* `updatedAt`: DateTime - Timestamp of last update.
* `conversationId`: String (required, primary key) - ID of the associated conversation.
* `summary`: Dict - Summary of the conversation.


### ModelInfos

```python
class ModelInfos(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    conversationId = StringField(required=True, primary_key=True)
    modelName = StringField()
    systemPrompt = StringField()
    inputTokensCount = IntField()
    outputTokensCount = IntField()
```

Represents information about the model used in a conversation.

* `createdAt`: DateTime - Timestamp of creation.
* `updatedAt`: DateTime - Timestamp of last update.
* `conversationId`: String (required, primary key) - ID of the associated conversation.
* `modelName`: String - Name of the model.
* `systemPrompt`: String - System prompt used.
* `inputTokensCount`: Int - Number of input tokens.
* `outputTokensCount`: Int - Number of output tokens.


### Prompts

```python
class Prompts(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    name = StringField(required=True)
    body = StringField(required=True)
    modelSettings = DictField()
```

Represents a prompt.

* `createdAt`: DateTime - Timestamp of creation.
* `updatedAt`: DateTime - Timestamp of last update.
* `name`: String (required) - Name of the prompt.
* `body`: String (required) - Body of the prompt.
* `modelSettings`: Dict - Model settings.

**Note:**  The `ProfileTypes`, `Dialers`, and `CallTypes` enums are assumed to be defined in the `..enums` module.  The specific values within these enums are not detailed here.
