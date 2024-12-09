from os.path import join

from src.db.models import Personas, Prompts
from src.db.schemas import Persona
from src.enums import CallTypes
from src.config import config
from src.logger import Logger

logger = Logger("prompts")


def resolve_prompt_name(
    promptType: str,
    callType: str,
    callScenario: str = "default",
    difficultyLevel: str = "default",
):
    return "_".join([promptType, callType, callScenario, difficultyLevel])


# For Live Call
defaultPersona = Persona(
    personaName="default",
    callScenario="default",
    difficultyLevel="default",
    linkedInUrl="default",
)


def get_prompt_from_file(prompt_name: str):
    return open(join(config["PROMPTS_PATH"], prompt_name), "r").read()


def get_prompt(
    promptType: str,
    callType: CallTypes,
    persona: Persona | Personas = defaultPersona,
    defaultPromptFile: str = "",
):
    promptName = resolve_prompt_name(
        promptType, callType.value, persona.callScenario, persona.difficultyLevel
    )
    logger.debug(f"Attempting to find {promptName} prompt.")
    prompt: Prompts = Prompts.objects(name=promptName).order_by("-updatedAt").first()

    if prompt:
        return prompt.body
    else:
        logger.error(
            "Unable to find Prompt in DB, attempting default Prompt from File."
        )
        return get_prompt_from_file(defaultPromptFile)
