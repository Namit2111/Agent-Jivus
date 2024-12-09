import json
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import openai
import requests
from os.path import join

from src.db.schemas import User
from src.db.utils import authenticate_user
from src.logger import Logger
from src.config import config
from src.enums import CallTypes, ProfileTypes
from src.utils.prompts import get_prompt
from src.utils.website_scraper import scrape_url
from src.utils.prompt_formatter import PromptTemplate
from src.db.subroutes.personas import get_persona
from src.db.models import (
    LinkedInInfos,
    ModelInfos,
    ProductInfos,
    ProfileInfos,
)

logger = Logger("prompt_utils")
openai.api_key = config["OPENAI_API_KEY"]


def get_linkedin_profile_nubela(linkedin_url):
    if config["USE_NUBELA"]:
        headers = {"Authorization": "Bearer " + config["NUBELA_API_KEY"]}
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        params = {
            "linkedin_profile_url": linkedin_url,
            "fallback_to_cache": "on-error",
            "use_cache": "if-present",
            "skills": "exclude",
            "inferred_salary": "exclude",
            "personal_email": "exclude",
            "personal_contact_number": "exclude",
            "twitter_profile_id": "exclude",
            "facebook_profile_id": "exclude",
            "github_profile_id": "exclude",
            "extra": "exclude",
        }

        response = requests.get(api_endpoint, params=params, headers=headers)
        response = response.json()
        if response.get("code", 200) != 200:
            raise Exception(f"Error in getting LinkedIN profile: {response}")
    else:
        with open(
            join(config["PROMPTS_PATH"], "sample_linkedin_profile.json"), "r"
        ) as f:
            response = json.load(f)
    return response


def linkedin_summary_generation(url: str):
    linkedin_summary_prompt = PromptTemplate(
        get_prompt(
            promptType="linkedin_summary",
            callType=CallTypes.IRRELEVANT,
            defaultPromptFile="linkedin_summary_prompt.txt",
        )
    )
    linkedin_api_response = get_linkedin_profile_nubela(linkedin_url=url)
    logger.debug(f"linkedin_api_response: {linkedin_api_response}")

    linkedin_summary_prompt = linkedin_summary_prompt.fill_slots(
        {"LinkedIn_APIResponse": str(linkedin_api_response)}
    )

    with open(
        join(config["PARAMETER_SCHEMAS_PATH"], "linkedin_summary_schema.json"), "r"
    ) as schema_file:
        linkedin_summary_schema = json.load(schema_file)
    messages = [
        {"role": "system", "content": "you are a virtual assistant"},
        {"role": "user", "content": linkedin_summary_prompt},
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_response",
                "parameters": linkedin_summary_schema,
            },
        }
    ]

    completion = openai.chat.completions.create(
        model=config["OPENAI_DEFAULT_MODEL_NAME"],
        messages=messages,  # type: ignore
        tools=tools,  # type: ignore
        tool_choice={"type": "function", "function": {"name": "generate_response"}},
        temperature=config["OPENAI_DEFAULT_TEMPERATURE"],
        top_p=config["OPENAI_DEFAULT_TOP_P"],
        frequency_penalty=config["OPENAI_DEFAULT_FREQUENCY_PENALTY"],
        presence_penalty=config["OPENAI_DEFAULT_PRESENCE_PENALTY"],
    )

    raw_data_str = completion.choices[0].message.tool_calls[0].function.arguments  # type: ignore
    logger.debug(f"raw_data_str: {raw_data_str}")
    llm_response = json.loads(raw_data_str)

    return linkedin_api_response, llm_response["personality_summary"], llm_response["buying_style"]


def website_summary_generation(url: str = ""):
    website_summary_prompt = PromptTemplate(
        get_prompt(
            promptType="website_summary",
            callType=CallTypes.IRRELEVANT,
            defaultPromptFile="website_summary_prompt.txt",
        )
    )

    if url:  # TODO: Remove this, its useless.
        website_api_response = {"Website_text_Dump": scrape_url(url)}
    else:
        website_api_response = {
            "Website_text_Dump": get_prompt(
                promptType="dummy_website_dump",
                callType=CallTypes.IRRELEVANT,
                defaultPromptFile="dummy_website_dump.txt",
            )
        }

    website_summary_prompt = website_summary_prompt.fill_slots(website_api_response)

    with open(
        join(config["PARAMETER_SCHEMAS_PATH"], "website_summary_schema.json"), "r"
    ) as schema_file:
        website_summary_schema = json.load(schema_file)
    messages = [
        {"role": "system", "content": "you are a virtual assistant"},
        {"role": "user", "content": website_summary_prompt},
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_response",
                "parameters": website_summary_schema,
            },
        }
    ]

    completion = openai.chat.completions.create(
        model=config["OPENAI_DEFAULT_MODEL_NAME"],
        messages=messages,  # type: ignore
        tools=tools,  # type: ignore
        tool_choice={"type": "function", "function": {"name": "generate_response"}},
        temperature=config["WEBSITE_SUMMARY_GENERATION_TEMPERATURE"],
        top_p=config["WEBSITE_SUMMARY_GENERATION_TOP_P"],
        frequency_penalty=config["WEBSITE_SUMMARY_GENERATION_FREQUENCY_PENALTY"],
        presence_penalty=config["WEBSITE_SUMMARY_GENERATION_PRESENCE_PENALTY"],
    )

    raw_data_str = completion.choices[0].message.tool_calls[0].function.arguments  # type: ignore
    logger.debug(f"raw_data_str: {raw_data_str}")
    llm_response = json.loads(raw_data_str)

    return website_api_response, llm_response["product_description"]


def get_persona_profile_info(persona):
    persona_profile_info_obj = ProfileInfos.objects(profileId=str(persona.id)).first()

    if persona.linkedInUrl:
        if persona_profile_info_obj is None:
            linkedin_api_resp, linkedin_summary,buyingStyleInfo = linkedin_summary_generation(
                persona.linkedInUrl
            )
            persona_profile_info_obj = ProfileInfos(
                profileType=ProfileTypes.PERSONA,
                profileId=str(persona.id),
                linkedinInfo=LinkedInInfos(
                    url=persona.linkedInUrl,
                    data=linkedin_api_resp,
                    summary=linkedin_summary,
                    buyingStyle=buyingStyleInfo
                ),
            )
            persona_profile_info_obj.save()
        else:
            if persona.linkedInUrl != persona_profile_info_obj.linkedinInfo.url:
                linkedin_api_resp, linkedin_summary,buyingStyleInfo = linkedin_summary_generation(
                    persona.linkedInUrl
                )
                persona_profile_info_obj.modify(
                    linkedinInfo=LinkedInInfos(
                        url=persona.linkedInUrl,
                        data=linkedin_api_resp,
                        summary=linkedin_summary,
                        buyingStyle=buyingStyleInfo
                    )
                )
                persona_profile_info_obj.reload()
            linkedin_api_resp = persona_profile_info_obj.linkedinInfo.data
            linkedin_summary = persona_profile_info_obj.linkedinInfo.summary
            buyingStyleInfo = persona_profile_info_obj.linkedinInfo.buyingStyle
    return linkedin_api_resp, linkedin_summary,buyingStyleInfo


def training_call_prompt_generation(persona_id, user_info: User):
    logger.debug("Generating training call prompt")
    persona = get_persona(persona_id=persona_id)

    # Defaults
    website_summary = "No Product Pitch Available"
    linkedin_api_resp = {
        "full_name": "Prospect name",
        "occupation": "Prospect occupation",
    }
    linkedin_summary = "No summary available"

    # TODO: Phase out this If Else tree. get_prompt() can directly take persona object.
    if persona.callScenario == "cold call":
        promptFileName = f"training_call_prompt_cold_call_{persona.difficultyLevel}.txt"
        training_call_prompt = PromptTemplate(
            get_prompt(
                promptType="conversation",
                callType=CallTypes.TRAINING_CALL,
                persona=persona,
                defaultPromptFile=promptFileName,
            )
        )
    elif persona.callScenario == "discovery call":
        training_call_prompt = PromptTemplate(
            get_prompt(
                promptType="conversation",
                callType=CallTypes.TRAINING_CALL,
                persona=persona,
                defaultPromptFile="training_call_prompt_discovery_call.txt",
            )
        )
    else:
        training_call_prompt = PromptTemplate(
            get_prompt(
                promptType="conversation",
                callType=CallTypes.TRAINING_CALL,
                persona=persona,
                defaultPromptFile="training_call_prompt.txt",
            )
        )

    linkedin_api_resp, linkedin_summary,_ = get_persona_profile_info(persona)

    user_profile_info_obj = ProfileInfos.objects(profileId=str(persona.userId)).first()

    if user_info.companyUrl:
        if user_profile_info_obj is None:
            website_api_resp, website_summary = website_summary_generation(
                url=user_info.companyUrl
            )
            user_profile_info_obj = ProfileInfos(
                profileType=ProfileTypes.USER,
                profileId=str(user_info.id),
                productInfo=ProductInfos(
                    url=user_info.companyUrl,
                    data=website_api_resp,
                    summary=website_summary,
                ),
            )
            logger.debug(f"user_profile_info_obj: {user_profile_info_obj}")
            user_profile_info_obj.save()
        else:
            if user_info.companyUrl != user_profile_info_obj.productInfo.url:
                website_api_resp, website_summary = website_summary_generation(
                    url=user_info.companyUrl
                )
                user_profile_info_obj.modify(
                    productInfo=ProductInfos(
                        url=user_info.companyUrl,
                        data=website_api_resp,
                        summary=website_summary,
                    )
                )
                user_profile_info_obj.reload()
            website_api_resp = user_profile_info_obj.productInfo.data
            website_summary = user_profile_info_obj.productInfo.summary
    logger.debug(f"linkedin_api_resp: {linkedin_api_resp}")
    final_prompt = training_call_prompt.fill_slots(
        {
            "Product Pitch": website_summary,
            "Prospect Name": linkedin_api_resp["full_name"],
            "Prospect Designation": linkedin_api_resp["occupation"],
            "Prospect Personality Summary from LinkedIn": linkedin_summary,
            "Call Scenario": persona.callScenario,
        }
    )
    return final_prompt


def get_training_call_prompt(conversation_id: str):
    training_call_prompt = (
        ModelInfos.objects(conversationId=conversation_id).first().systemPrompt
    )
    return training_call_prompt


def get_linkedin_profile_prospeo(linkedin_url):
    url = "https://api.prospeo.io/linkedin-email-finder"
    api_key = config["PROSPEO_API_KEY"]

    required_headers = {"Content-Type": "application/json", "X-KEY": api_key}
    data = {"url": linkedin_url}

    response = requests.post(url, json=data, headers=required_headers)
    return response.json()["response"]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_auth_response(auth_token: str = Depends(oauth2_scheme)) -> dict:
    auth_response = authenticate_user(auth_token)
    if auth_response.get("status") != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=auth_response.get("message", "Invalid user auth token"),
        )
    return auth_response
