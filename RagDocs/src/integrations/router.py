import base64
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from starlette.responses import Response
from starlette.datastructures import URL
import requests

from src.config import config
from src.integrations.hubspot import objects
from src.integrations.email_provider.gmail import router as gmail
from src.integrations.email_provider.smtp import router as smtp
from src.integrations.Calendly import router as calendly
from src.db.models import Integrations
from src.db.utils import authenticate_user
from src.live_call.schemas import (
    CalendlyIntegrationSetupRequest,
    GmailIntegrationSetupRequest,
    HubspotIntegrationSetupRequest,
    SMTPIntegrationSetupRequest,
    ZoomIntegrationSetupRequest,
)
from datetime import datetime, timedelta

router = APIRouter(prefix="/integrations", tags=["integrations"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# @router.get("/hubspot_callback")
# async def hubspot_callback(request: Request):
#     # Extract the 'code' query parameter
#     code = request.query_params.get('code')

#     if not code:
#         raise HTTPException(status_code=400, detail="Authorization code missing")

#     try:
#         # Exchange the authorization code for access and refresh tokens
#         response = requests.post(
#             'https://api.hubapi.com/oauth/v1/token',
#             params={
#                 'grant_type': 'authorization_code',
#                 'client_id': config('HUBSPOT_CLIENT_ID'),
#                 'client_secret': config('HUBSPOT_CLIENT_SECRET'),
#                 'redirect_uri': config('HUBSPOT_REDIRECT_URI'),
#                 'code': code,
#             },
#         )

#         response_data = response.json()
#         access_token = response_data.get('access_token')
#         refresh_token = response_data.get('refresh_token')
#         expires_in = response_data.get('expires_in')

#         integration = Integrations(
#                 service="hubspot",
#                 data={
#                     "hubspot_api_key": setup_data.hubspot_api_key,
#                 },
#                 userId=user_id,
#             ).save()

#         print(response_data)

#         if not access_token or not refresh_token:
#             raise HTTPException(status_code=500, detail="Failed to obtain tokens")

#         # Set tokens in cookies
#         response = RedirectResponse(url="http://localhost:3000/dashboard/hubspot-developer")
#         return response

#     except requests.HTTPError as error:
#         print(f"Error exchanging code for tokens: {error}")
#         return RedirectResponse(url=f"http://localhost:3000/dashboard/hubspot-developer?status=error&message=Error during token exchange")

@router.post("/hubspot_integration_setup")
async def hubspot_integration_setup(
    setup_data: HubspotIntegrationSetupRequest,  # Using the Pydantic model for request body
    auth_token: str = Depends(oauth2_scheme),
):
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            # You might want to use a more appropriate status code like 401 for Unauthorized
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )

        user_id = auth_response.get("user_info").get("id")  # type:ignore

        try:
            # Check if a record with the same user_id already exists
            existing_integration = Integrations.objects(
                userId=user_id, service="hubspot"
            ).first()

            if existing_integration:
                # A record with the same user_id already exists, so you can handle this situation
                # For example, you can raise an exception or return an error response
                # raise Exception("Integration for this user already exists")
                existing_integration.update(
                    data={
                        # "hubspot_api_key": setup_data.hubspot_api_key,
                        "access_token": setup_data.access_token,
                        "refresh_token": setup_data.refresh_token,
                        "expires_in": setup_data.expires_in ,
                    },
                )
            else:
                # Here, save the integration details and handle any potential errors
                integration = Integrations(
                    service="hubspot",
                    data={
                        # "hubspot_api_key": setup_data.hubspot_api_key,
                        "access_token": setup_data.access_token,
                        "refresh_token": setup_data.refresh_token,
                        "expires_in": setup_data.expires_in,
                    },
                    userId=user_id,
                ).save()
        except Exception as exp:
            HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="integration update failed",
            )
        # Return a 200 OK response with a success message
        return {"message": "Hubspot integration setup successful"}

    except HTTPException as http_exc:
        # Re-raise the HTTPException if it's been explicitly raised
        raise http_exc
    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/gmail_integration_setup")
async def gmail_integration_setup(
    setup_data: GmailIntegrationSetupRequest,  # Using the Pydantic model for request body
    auth_token: str = Depends(oauth2_scheme),
):
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            # You might want to use a more appropriate status code like 401 for Unauthorized
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )

        user_id = auth_response.get("user_info").get("id")  # type:ignore

        try:
            # Check if a record with the same user_id already exists
            existing_integration = Integrations.objects(
                userId=user_id, service="gmail"
            ).first()

            if existing_integration:
                # A record with the same user_id already exists, so you can handle this situation
                # For example, you can raise an exception or return an error response
                # raise Exception("Integration for this user already exists")
                existing_integration.update(
                    data={
                        # "hubspot_api_key": setup_data.hubspot_api_key,
                        "access_token": setup_data.access_token,
                        "refresh_token": setup_data.refresh_token,
                        "expires_in": setup_data.expires_in ,
                    },
                )
            else:
                # Here, save the integration details and handle any potential errors
                integration = Integrations(
                    service="gmail",
                    data={
                        # "hubspot_api_key": setup_data.hubspot_api_key,
                        "access_token": setup_data.access_token,
                        "refresh_token": setup_data.refresh_token,
                        "expires_in": setup_data.expires_in,
                    },
                    userId=user_id,
                ).save()
        except Exception as exp:
            HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="integration update failed",
            )
        # Return a 200 OK response with a success message
        return {"message": "Gmail integration setup successful"}

    except HTTPException as http_exc:
        # Re-raise the HTTPException if it's been explicitly raised
        raise http_exc
    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/smtp_integration_setup")
async def smtp_integration_setup(
    setup_data: SMTPIntegrationSetupRequest,  # Using the Pydantic model for request body
    auth_token: str = Depends(oauth2_scheme),
):
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            # You might want to use a more appropriate status code like 401 for Unauthorized
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )

        user_id = auth_response.get("user_info").get("id")  # type:ignore

        try:
            # Check if a record with the same user_id already exists
            existing_integration = Integrations.objects(
                userId=user_id, service="smtp"
            ).first()

            if existing_integration:
                # A record with the same user_id already exists, so you can handle this situation
                # For example, you can raise an exception or return an error response
                # raise Exception("Integration for this user already exists")
                existing_integration.update(
                    data={
                        # "hubspot_api_key": setup_data.hubspot_api_key,
                        "email": setup_data.email,
                        "smtpPassword": setup_data.smtp_password,
                    },
                )
            else:
                # Here, save the integration details and handle any potential errors
                integration = Integrations(
                    service="smtp",
                    data={
                        # "hubspot_api_key": setup_data.hubspot_api_key,
                        "email": setup_data.email,
                        "smtpPassword": setup_data.smtp_password,
                    },
                    userId=user_id,
                ).save()
        except Exception as exp:
            HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="integration update failed",
            )
        # Return a 200 OK response with a success message
        return {"message": "SMTP integration setup successful"}

    except HTTPException as http_exc:
        # Re-raise the HTTPException if it's been explicitly raised
        raise http_exc
    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/calendly_integration_setup")
async def calendly_integration_setup(
    setup_data: CalendlyIntegrationSetupRequest,  # Using the Pydantic model for request body
    auth_token: str = Depends(oauth2_scheme),
):
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            # You might want to use a more appropriate status code like 401 for Unauthorized
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )

        user_id = auth_response.get("user_info").get("id")  # type:ignore

        try:
            # Check if a record with the same user_id already exists
            existing_integration = Integrations.objects(
                userId=user_id, service="calendly"
            ).first()

            if existing_integration:
                # A record with the same user_id already exists, so you can handle this situation
                # For example, you can raise an exception or return an error response
                # raise Exception("Integration for this user already exists")
                existing_integration.update(
                    data={
                        "pat_token": setup_data.pat_token,
                    },
                )
            else:
                # Here, save the integration details and handle any potential errors
                integration = Integrations(
                    service="calendly",
                    data={
                        "pat_token": setup_data.pat_token,
                    },
                    userId=user_id,
                ).save()
        except Exception as exp:
            HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="integration update failed",
            )
        # Return a 200 OK response with a success message
        return {"message": "Calendly integration setup successful"}

    except HTTPException as http_exc:
        # Re-raise the HTTPException if it's been explicitly raised
        raise http_exc
    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/zoom_integration_setup")
async def zoom_integration_setup(
    setup_data: ZoomIntegrationSetupRequest,  # Using the Pydantic model for request body
    auth_token: str = Depends(oauth2_scheme),
):
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            # You might want to use a more appropriate status code like 401 for Unauthorized
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=auth_response.get("message", "Invalid user auth token"),
            )

        user_id = auth_response.get("user_info").get("id")  # type:ignore

        # Endpoint for obtaining an access token
        TOKEN_URL = "https://zoom.us/oauth/token"

        try:
            # Data to be sent when requesting an access token
            token_data = {
                "grant_type": "client_credentials",
                "client_id": setup_data.client_id,
                "client_secret": setup_data.client_secret,
            }

            # Try to obtain an access token using the provided credentials
            # try:
            response = requests.post(TOKEN_URL, data=token_data)
            response_data = response.json()

            if response.status_code != 200:
                # If the response status code is not 200, raise an exception with the error message
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid Client ID/Secret",
                )

        except HTTPException as http_exc:
            # Re-raise the HTTPException if it's been explicitly raised
            raise http_exc
        except Exception as exp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Client ID/Secret",
            )

        headers = {
            "Authorization": f"Basic {base64.b64encode((setup_data.client_id + ':' + setup_data.client_secret).encode('utf-8')).decode('utf-8')}"
        }

        payload = {
            "grant_type": "account_credentials",
            "account_id": setup_data.account_id,
        }
        response = requests.post(TOKEN_URL, headers=headers, data=payload)
        response_data = response.json()

        if response.status_code != 200:
            # If the response status code is not 200, raise an exception with the error message
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response_data.get("message", "Invalid account ID"),
            )

        try:
            # Check if a record with the same user_id already exists
            existing_integration = Integrations.objects(
                userId=user_id, service="zoom"
            ).first()

            if existing_integration:
                # A record with the same user_id already exists, so you can handle this situation
                # For example, you can raise an exception or return an error response
                raise Exception("Integration for this user already exists")

            # Here, save the integration details and handle any potential errors
            integration = Integrations(
                service="zoom",
                data={
                    "client_id": setup_data.client_id,
                    "client_secret": setup_data.client_secret,
                    "account_id": setup_data.account_id,
                },
                userId=user_id,
            ).save()
        except Exception as exp:
            HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="integration update failed",
            )
        # Return a 200 OK response with a success message
        return {"message": "Zoom integration setup successful"}

    except HTTPException as http_exc:
        # Re-raise the HTTPException if it's been explicitly raised
        raise http_exc
    except Exception as e:
        # Handle other exceptions and return an appropriate error code
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/user/integration", status_code=200)
async def get_integration_status(auth_token: str = Depends(oauth2_scheme)):
    supported_integrations = ["zoom", "hubspot", "gmail", "outlook", "smtp", "calendly"]
    try:
        auth_response = authenticate_user(auth_token)
        if auth_response.get("status") != 200:
            raise ValueError(auth_response.get("message", "Invalid user auth token"))

        user_id = auth_response.get("user_info").get("id")  # type:ignore

        response = {}

        for service_name in supported_integrations:
            existing_integration = Integrations.objects(
                userId=user_id, service=service_name
            ).first()
            if existing_integration:
                response[service_name] = True
            else:
                response[service_name] = False

        return response

    except ValueError as ve:
        # Handle known errors
        raise HTTPException(status_code=409, detail=str(ve))
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=500, detail=str(e))


router.include_router(objects.router)
router.include_router(gmail.router)
router.include_router(smtp.router)
router.include_router(calendly.router)
