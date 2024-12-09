from datetime import datetime
from src.logger import Logger
from src.db.schemas import LiveInsight, LiveInsightsResponse
from src.db.utils import handle_error, valid_conversation_id
from src.db.models import LiveInsights
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/live-insights", tags=["live-insights"])
logger = Logger("live_insights")


def get_live_insight(conversation_id: str = Depends(valid_conversation_id)):
    liveInsight = LiveInsights.objects(conversationId=conversation_id).first()
    assert liveInsight
    return liveInsight


@router.get("/{conversation_id}", response_model=LiveInsightsResponse)
def read_live_insight(conversation_id: str = Depends(valid_conversation_id)):
    try:
        liveInsight = get_live_insight(conversation_id)
        return LiveInsightsResponse(**liveInsight.to_mongo(use_db_field=False))
    except Exception as e:
        handle_error(e)


@router.post("/{conversation_id}", response_model=LiveInsightsResponse)
def create_live_insight(
    insights: LiveInsight, conversation_id: str = Depends(valid_conversation_id)
):
    try:
        liveInsight = LiveInsights(conversationId=conversation_id, insights=insights)
        liveInsight = liveInsight.save()
        return LiveInsightsResponse(**liveInsight.to_mongo(use_db_field=False))
    except Exception as e:
        handle_error(e)


@router.put("/{conversation_id}", response_model=LiveInsightsResponse)
def update_live_insight(conversation_id: str, insight_dict: dict) -> bool:
    try:
        liveInsight = get_live_insight(conversation_id)
        liveInsight.update(updatedAt=datetime.now())
        liveInsight.update(push__insights=insight_dict)
        return True
    except Exception as e:
        handle_error(e)
        return False


@router.delete("/{conversation_id}")
def delete_summary(conversation_id: str = Depends(valid_conversation_id)):
    try:
        liveInsights = get_live_insight(conversation_id)
        liveInsights.delete()
        return {"message": "success"}
    except Exception as e:
        handle_error(e)
