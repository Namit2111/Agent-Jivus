from enum import Enum


class ProfileTypes(Enum):
    USER = "user"
    PERSONA = "persona"


class Dialers(Enum):
    ZOOM = "zoom"
    WEB = "web"


class CallTypes(Enum):
    TRAINING_CALL = "training_call"
    LIVE_CALL = "live_call"
    IRRELEVANT = "irrelevant"


class UserRoles(Enum):
    SUPER_ADMIN = "superadmin"
    ADMIN = "admin"
    MANAGER = "manager"
    AGENT = "agent"
