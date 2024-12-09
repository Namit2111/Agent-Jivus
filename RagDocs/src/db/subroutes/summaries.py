from datetime import datetime
from src.db.schemas import SummariesResponse, Summary
from src.db.utils import handle_error, valid_conversation_id
from src.db.models import Summaries
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/summaries", tags=["summaries"])


def get_summary(conversation_id: str = Depends(valid_conversation_id)):
    summary = Summaries.objects(conversationId=conversation_id).first()
    assert summary
    return summary


@router.get("/{conversation_id}", response_model=SummariesResponse)
def read_summary(conversation_id: str = Depends(valid_conversation_id)):
    try:
        summary = get_summary(conversation_id)
        return SummariesResponse(**summary.to_mongo(use_db_field=False))
    except Exception as e:
        handle_error(e)


@router.post("/{conversation_id}", response_model=SummariesResponse)
def create_summary(
    summary_in: Summary, conversation_id: str = Depends(valid_conversation_id)
):
    try:
        summary = Summaries(conversationId=conversation_id, summary=summary_in)
        summary = summary.save()
        return SummariesResponse(**summary.to_mongo(use_db_field=False))
    except Exception as e:
        handle_error(e)


@router.put("/{conversation_id}", response_model=SummariesResponse)
def update_summary(
    new_summary: Summary, conversation_id: str = Depends(valid_conversation_id)
):
    try:
        summary = get_summary(conversation_id)
        summary_update_status = summary.modify(
            updatedAt=datetime.now(), summary=new_summary
        )
        if summary_update_status:
            summary.reload()
            return SummariesResponse(**summary.to_mongo(use_db_field=False))
        else:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="Unable to modify summary document.",
            )
    except Exception as e:
        handle_error(e)


@router.delete("/{conversation_id}")
def delete_summary(conversation_id: str = Depends(valid_conversation_id)):
    try:
        summary = get_summary(conversation_id)
        summary.delete()
        return {"message": "success"}
    except Exception as e:
        handle_error(e)
