```markdown
# ConversationCreateReq

This module defines the `ConversationCreateReq` Pydantic model used for creating conversations.

## Class: `ConversationCreateReq`

This class represents the request body for creating a new conversation.  It uses the Pydantic library for data validation and parsing.

**Import:**

```python
from pydantic import BaseModel
```

**Class Definition:**

```python
class ConversationCreateReq(BaseModel):
    conversationId: str
    personaId: str
```

**Fields:**

* **`conversationId: str`**:  A string representing the unique identifier for the conversation.  *Required*.
* **`personaId: str`**: A string representing the unique identifier for the persona involved in the conversation. *Required*.


**Example Usage:**

```python
from your_module import ConversationCreateReq  # Replace your_module

request_data = ConversationCreateReq(conversationId="conv-123", personaId="persona-456")

# Accessing fields:
conversation_id = request_data.conversationId
persona_id = request_data.personaId

print(f"Conversation ID: {conversation_id}, Persona ID: {persona_id}")
```

**Error Handling:**

Pydantic automatically handles validation. If the input data does not conform to the defined types, a `ValidationError` will be raised.  For example, providing a non-string value for `conversationId` or `personaId` will result in an error.
```

```python
try:
    invalid_request = ConversationCreateReq(conversationId=123, personaId="persona-456")
except ValidationError as e:
    print(f"Validation Error: {e}")
```
```
