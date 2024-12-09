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


class FullDocumentQuerySet(QuerySet):
    def full(self):
        return [doc.full() for doc in self]


class Personas(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    personaName = StringField(required=True, max_length=100)
    callScenario = StringField(required=True)
    difficultyLevel = StringField(required=True)
    userId = ObjectIdField(required=True)
    linkedInUrl = StringField(required=True)


# TODO: Convert to Document
class Integrations(DynamicDocument):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    service = StringField(required=True)
    data = DictField()
    userId = ObjectIdField(required=True)


class ProductInfos(EmbeddedDocument):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    url = URLField(required=True)
    data = DictField(required=True)
    summary = StringField(required=True)

class HubspotInfos(EmbeddedDocument):
    createdate = DateTimeField(default=datetime.now)
    lastmodifieddate = DateTimeField(default=datetime.now)
    email = StringField(required=True)
    email_chain = StringField(required=False)
    hs_linkedin_url = URLField(required=False)
    hs_object_id = StringField(required=True)
    notes = StringField(required=False)

class LinkedInInfos(EmbeddedDocument):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    url = URLField(required=True)
    data = DictField(required=True)
    summary = StringField(required=True)
    buyingStyle = StringField(required=True)


class ProfileInfos(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    profileType = EnumField(ProfileTypes, required=True)
    profileId = StringField(required=True)
    hubspotInfo = EmbeddedDocumentField(HubspotInfos)
    productInfo = EmbeddedDocumentField(ProductInfos)
    linkedinInfo = EmbeddedDocumentField(LinkedInInfos)


class Conversations(
    Document
):  # TODO: group redundant metadata fields (callScenario, callRecordingUrl, etc.) into metadata Field
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


class Transcripts(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    conversationId = StringField(required=True, primary_key=True)
    turns = ListField(DictField(), default=list)


class LiveInsights(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    conversationId = StringField(required=True, primary_key=True)
    insights = ListField(DictField(), default=list)


class Summaries(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    conversationId = StringField(required=True, primary_key=True)
    summary = DictField()


class ModelInfos(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    conversationId = StringField(required=True, primary_key=True)
    modelName = StringField()
    systemPrompt = StringField()
    inputTokensCount = IntField()
    outputTokensCount = IntField()


class Prompts(Document):
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)
    name = StringField(required=True)
    body = StringField(required=True)
    modelSettings = DictField()
