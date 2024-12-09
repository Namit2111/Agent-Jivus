# File: enums.py (Assumed Filename)

This file defines several Python enumerations (`Enum`) used to represent different categories and types within an application.  These enums provide type safety and improve code readability by using descriptive names instead of raw strings.

## Enumerations

* **`ProfileTypes`**:  Represents the types of profiles within the system.

    * `USER`: Represents a standard user profile.  Value: `"user"`
    * `PERSONA`: Represents a persona profile (likely a template or representative user). Value: `"persona"`

* **`Dialers`**: Represents the different dialer types available.

    * `ZOOM`: Represents the Zoom dialer. Value: `"zoom"`
    * `WEB`: Represents a web-based dialer. Value: `"web"`

* **`CallTypes`**: Represents the different types of calls.

    * `TRAINING_CALL`: Represents a training call. Value: `"training_call"`
    * `LIVE_CALL`: Represents a live call. Value: `"live_call"`
    * `IRRELEVANT`: Represents a call that is not relevant to the system's purpose. Value: `"irrelevant"`

* **`UserRoles`**: Represents the different roles a user can have within the system.

    * `SUPER_ADMIN`: Represents a super administrator with full access. Value: `"superadmin"`
    * `ADMIN`: Represents an administrator with elevated privileges. Value: `"admin"`
    * `MANAGER`: Represents a manager with specific management permissions. Value: `"manager"`
    * `AGENT`: Represents a standard agent. Value: `"agent"`


**Example Usage:**

```python
from enums import ProfileTypes, UserRoles

profile_type = ProfileTypes.PERSONA
print(profile_type.value)  # Output: persona

user_role = UserRoles.ADMIN
print(user_role) # Output: UserRoles.ADMIN
print(user_role.name) # Output: ADMIN
```
