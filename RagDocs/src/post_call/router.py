from fastapi import APIRouter, Depends, HTTPException, status
import requests

from src.config import config
from src.db.subroutes.summaries import update_summary
from src.db.models import Conversations, Summaries
from src.enums import CallTypes
from src.live_call.utils import live_call_summary_generation
from src.post_call.schemas import *
from src.logger import Logger
from src.post_call.utils import training_call_summary_generation

logger = Logger("post_call")

router = APIRouter()

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
NODE_BACKEND = config["NODE_BACKEND"]


def get_superadmin_token():
    try:
        resp = requests.post(
            f"{NODE_BACKEND}/auth/login",
            json={
                "email": config["SUPER_ADMIN_EMAIL"],
                "password": config["SUPER_ADMIN_PASSWORD"],
            },
        )
        logger.debug(f"response json under superadmin auth: {resp.json()}")
        if resp.status_code == 200:
            return resp.json().get("accessToken")
        else:
            raise ValueError("Failed to get superadmin token")
    except Exception as e:
        raise ValueError(str(e))


def get_user_org(token: str):
    try:
        resp = requests.get(
            f"{NODE_BACKEND}/memberships/user-org",
            headers={"Authorization": f"Bearer {token}"},
        )
        logger.debug(f"got user org: {resp.json()}")
        if resp.status_code == 200:
            return resp.json()
        else:
            raise ValueError("Failed to get user org")
    except Exception as e:
        raise ValueError(str(e))


SUPER_ADMIN_TOKEN = ""


def check_user_in_org(user_id: str, org_id: str):
    try:
        global SUPER_ADMIN_TOKEN
        if not SUPER_ADMIN_TOKEN:
            SUPER_ADMIN_TOKEN = get_superadmin_token()
        resp = requests.get(
            f"{NODE_BACKEND}/memberships/check-user-in-org",
            params={"userId": user_id},
            headers={
                "Authorization": f"Bearer {SUPER_ADMIN_TOKEN}",
                "x-org-id": org_id,
            },
        )
        if resp.status_code == 403:
            SUPER_ADMIN_TOKEN = get_superadmin_token()
            resp = requests.get(
                f"{NODE_BACKEND}/memberships/check-user-in-org",
                params={"userId": user_id},
                headers={
                    "Authorization": f"Bearer {SUPER_ADMIN_TOKEN}",
                    "x-org-id": org_id,
                },
            )
        if resp.status_code == 200:
            return resp.json()
        else:
            raise ValueError("Failed to check user in org")
    except Exception as e:
        raise ValueError(str(e))


def authenticate_user(token: str):
    try:
        resp = requests.get(
            f"{NODE_BACKEND}/user/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        if resp.status_code == 200:
            x_org_id = resp.headers.get("x-org-id")
            return {
                "status": 200,
                "message": "Authentication successful",
                "user_info": resp.json(),
                "x_org_id": x_org_id,
            }
        else:
            return {
                "status": 400,
                "message": "Authentication failed",
            }
    except Exception as e:
        raise ValueError(str(e))


@router.post(
    "/post_call_analytics",
    response_model=List[
        Union[
            AnalyticsRoleplayDuration,
            AnalyticsRoleplayTypes,
            AnalyticsSalesCallOutcomes,
            AnalyticsOverallCallPerformanceTeam,
            AnalyticsOverallCallPerformanceUser,
            AnalyticsOverallCallStagePerformance,
            AnalyticsMostCommonObjection,
            AnalyticsMostCommonObjectionResponse,
            AnalyticsExpertAttributes,
            AnalyticsStruggleAttributes,
            AnalyticsSuggestionsForImprovement,
        ]
    ],
)
async def post_call_analytics(
    post_call_analytics_request: PostCallAnalyticsRequest,
    auth_token: str = Depends(oauth2_scheme),
):
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )

        user_id = auth_response.get("user_info").get("id")  # type: ignore
        role = auth_response.get("user_info").get("role")  # type: ignore
        org_id = get_user_org(auth_token).get("id")

        if not check_user_in_org(user_id, org_id):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is not in the organization",
            )

        if role == "manager":
            analytics_overall_call_performance = AnalyticsOverallCallPerformanceTeam(
                heading="Overall Call Performance",
                type=ChartType.BAR,
                data={
                    "labels": ["User 1", "User 2", "User 3", "User 4"],
                    "data": [10, 20, 30, 40],
                },
            )
        elif role == "agent":
            analytics_overall_call_performance = AnalyticsOverallCallPerformanceUser(
                heading="Overall Call Performance",
                type=ChartType.METER,
                data={
                    "levels": "5",
                    "percent": "0.8",
                },
            )

        analytics_report = [
            AnalyticsRoleplayDuration(
                heading="Roleplay Duration",
                type=ChartType.TEXT,
                data={
                    "daily": "230",
                    "weekly": "230",
                },
            ),
            AnalyticsRoleplayTypes(
                heading="Roleplay Types",
                type=ChartType.PIE,
                data={
                    "labels": ["Cold Call", "Discovery Call", "Demo Call"],
                    "data": [10, 20, 30],
                },
            ),
            AnalyticsSalesCallOutcomes(
                heading="Sales call Outcomes",
                type=ChartType.PIE,
                data={
                    "labels": ["Interested", "No answer", "Voicemail"],
                    "data": [25, 25, 50],
                },
            ),
            analytics_overall_call_performance,
            AnalyticsOverallCallStagePerformance(
                heading="Overall Call Stage Performance",
                type=ChartType.BAR,
                data={
                    "labels": ["Stage 1", "Stage 2", "Stage 3", "Stage 4"],
                    "data": [10, 20, 30, 40],
                },
            ),
            AnalyticsMostCommonObjection(
                heading="Most Common Objection",
                type=ChartType.TEXT,
                data={  # cSpell:disable
                    "data": "Dummy most common objection: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. "
                },  # cSpell:enable
            ),
            AnalyticsMostCommonObjectionResponse(
                heading="Response for Most Common Objection",
                type=ChartType.TEXT,
                data={  # cSpell:disable
                    "data": "Dummy response for most common objection: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. "
                },  # cSpell:enable
            ),
            AnalyticsExpertAttributes(
                heading="Expert Attributes",
                type=ChartType.TEXT,
                data={  # cSpell:disable
                    "data": "Dummy expert attributes: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus."
                },  # cSpell:enable
            ),
            AnalyticsStruggleAttributes(
                heading="Struggle Attributes",
                type=ChartType.TEXT,
                data={  # cSpell:disable
                    "data": "Dummy struggle attributes: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. "
                },  # cSpell:enable
            ),
            AnalyticsSuggestionsForImprovement(
                heading="Suggestions for Improvement",
                type=ChartType.TEXT,
                data={  # cSpell:disable
                    "data": "Dummy suggestions for Improvement: Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus."
                },  # cSpell:enable
            ),
        ]

        return analytics_report
    except HTTPException as http_exc:
        # Re-raise the HTTPException if it's been explicitly raised
        raise http_exc
    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/get_summary")
async def get_summary(conversation_id: str, auth_token: str = Depends(oauth2_scheme)):
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )

        # userId = auth_response.get("user_info").get("id") # TODO: Remove | Why use userID here at all? there will only be 1 conversation.
        conversation: Conversations = Conversations.objects(
            conversationId=conversation_id
        ).first()
        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )
        if str(conversation.userId) != auth_response["user_info"]["id"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Conversation does not belong to the user",
            )
        summary_obj: Summaries = Summaries.objects(
            conversationId=conversation.conversationId
        ).first()
        
        if conversation.callType == CallTypes.TRAINING_CALL:
            if not summary_obj.summary:
                generated_call_summary = training_call_summary_generation(
                    conversation.conversationId
                )
                summary_obj = update_summary(  # type: ignore
                    conversation_id=conversation.conversationId,
                    new_summary=generated_call_summary,
                )
            return {
                "conversationId": conversation.conversationId,
                "callTime": conversation.callDateTime,
                "callDuration": conversation.callDuration,
                "summary": summary_obj.summary,  # type: ignore
            }

        elif conversation.callType == CallTypes.LIVE_CALL:
            if not summary_obj.summary:
                generated_call_summary = live_call_summary_generation(
                    conversation.conversationId
                )
                summary_obj = update_summary(  # type: ignore
                    conversation_id=conversation.conversationId,
                    new_summary=generated_call_summary,
                )
            return {
                "conversationId": conversation.conversationId,
                "callTime": conversation.callDateTime,
                "callDuration": conversation.callDuration,
                "summary": summary_obj.summary,  # type: ignore
            }

    except HTTPException as http_exc:
        # Re-raise the HTTPException if it's been explicitly raised
        logger.error("An error occurred: %s", str(http_exc))
        raise http_exc
    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        logger.error("An error occurred: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}",
        )
