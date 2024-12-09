# Python File Documentation: models.py

This file defines the MongoDB models using `mongoengine` for various data structures related to conversations, profiles, and integrations.  It also includes custom queryset functionalities.

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
        Retrieves all documents in the queryset, populating related reference fields.

        Returns:
            list: A list of documents with related reference fields populated.  
                  WARNING:  Do not use the output of this function for Reference Fields.
        """
        return [doc.full() for doc in self]
```

## Models

### `Personas`

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

### `Integrations`

```python
class Integrations(DynamicDocument):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    service = StringField(required=True)
    data = DictField()
    userId = ObjectIdField(required=True)
```

Represents integrations with external services.  Uses `DynamicDocument` for flexibility.  **TODO:** Consider converting to a standard `Document`.

### `ProductInfos`

```python
class ProductInfos(EmbeddedDocument):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    url = URLField(required=True)
    data = DictField(required=True)
    summary = StringField(required=True)
```

Embedded document containing product information.

### `HubspotInfos`

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

### `LinkedInInfos`

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

### `ProfileInfos`

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

Represents profile information, potentially combining data from different sources.

### `Conversations`

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

Represents a conversation, including references to personas and profile information.  **TODO:** Group redundant metadata fields into a single `metadata` field.

### `Transcripts`

```python
class Transcripts(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    conversationId = StringField(required=True, primary_key=True)
    turns = ListField(DictField(), default=list)
```

Stores the transcript of a conversation.

### `LiveInsights`

```python
class LiveInsights(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    conversationId = StringField(required=True, primary_key=True)
    insights = ListField(DictField(), default=list)
```

Stores live insights generated during a conversation.

### `Summaries`

```python
class Summaries(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    conversationId = StringField(required=True, primary_key=True)
    summary = DictField()
```

Stores a summary of a conversation.

### `ModelInfos`

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

Stores information about the large language model used in a conversation.

### `Prompts`

```python
class Prompts(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    name = StringField(required=True)
    body = StringField(required=True)
    modelSettings = DictField()
```

Represents prompts used for the large language models.


This documentation provides a comprehensive overview of the data models defined in the `models.py` file.  Remember to replace  `ProfileTypes` and `Dialers`, `CallTypes` with the actual imports from `..enums`.
