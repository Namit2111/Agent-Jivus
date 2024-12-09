from src.config import config
from fastapi import APIRouter, Depends
from mongoengine import connect
from src.db.subroutes import (
    conversations,
    live_insights,
    personas,
    summaries,
    transcripts,
    prompts,
)
from src.utils.auth import get_auth_response

connect(db=config["DB_NAME"], host=config["DB_URI"])

router = APIRouter(prefix="/v1", dependencies=[Depends(get_auth_response)])

router.include_router(conversations.router)
router.include_router(live_insights.router)
router.include_router(personas.router)
router.include_router(summaries.router)
router.include_router(transcripts.router)
router.include_router(prompts.router)
