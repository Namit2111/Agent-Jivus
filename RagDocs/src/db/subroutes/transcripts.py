from datetime import datetime
from src.db.schemas import TranscriptResponse, TranscriptTurns
from src.db.utils import handle_error, valid_conversation_id
from src.db.models import Conversations, Transcripts
from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(prefix="/transcripts", tags=["transcripts"])


def get_transcript(conversation_id: str = Depends(valid_conversation_id)):
    transcript = Transcripts.objects(conversationId=conversation_id).first()
    assert transcript
    return transcript


@router.get("/{conversation_id}", response_model=TranscriptResponse)
def read_transcript(conversation_id: str = Depends(valid_conversation_id)):
    try:
        transcript = get_transcript(conversation_id)
        return TranscriptResponse(**transcript.to_mongo(use_db_field=False))
    except Exception as e:
        handle_error(e)


@router.post("/{conversation_id}", response_model=TranscriptResponse)
def create_transcript(
    turns: list[dict], conversation_id: str = Depends(valid_conversation_id)
):
    try:
        transcript = Transcripts(conversationId=conversation_id, turns=turns)
        transcript = transcript.save()
        return TranscriptResponse(**transcript.to_mongo(use_db_field=False))
    except Exception as e:
        handle_error(e)


@router.put("/{conversation_id}", response_model=TranscriptResponse)
def update_transcript(
    turns: list[dict], conversation_id: str = Depends(valid_conversation_id)
):
    try:
        transcripts = [
            {
                "speaker": msg.get("role"),
                "transcript": msg.get("content"),
                "start_time": msg.get("start_time"),
                "end_time": msg.get("end_time"),
            }
            for msg in turns
        ]
        transcript = get_transcript(conversation_id)
        transcript_update_status = transcript.modify(
            updatedAt=datetime.now(), turns=transcripts
        )
        transcript.reload()

        if transcript_update_status:
            return TranscriptResponse(**transcript.to_mongo(use_db_field=False))
        else:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="Unable to Update Transcript",
            )
    except Exception as e:
        handle_error(e)


@router.patch("/{conversation_id}", response_model=TranscriptResponse)
def patch_transcript(
    transcript_turn: TranscriptTurns,
    conversation_id: str = Depends(valid_conversation_id),
) -> bool:
    try:
        transcript = get_transcript(conversation_id)
        transcript.update(push__turns=transcript_turn)
        return True
    except Exception as e:
        handle_error(e)
        return False


@router.delete("/{conversation_id}")
def delete_transcript(conversation_id: str = Depends(valid_conversation_id)):
    try:
        transcript = get_transcript(conversation_id)
        transcript.delete()
        return {"message": "success"}
    except Exception as e:
        handle_error(e)
