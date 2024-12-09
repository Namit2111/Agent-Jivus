from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import AnyUrl

from src.db.models import LinkedInInfos, ProfileInfos
from src.db.schemas import HubspotInfo, LinkedInInfo, ProductInfo, ProfileInfo, ProfileInfoResponse
from src.db.utils import handle_error, valid_profile_id
from src.enums import ProfileTypes
from src.pre_call.utils import linkedin_summary_generation

router = APIRouter(prefix="/profile", tags=["personas"])


def get_profile(profile_id: str = Depends(valid_profile_id)):
    return ProfileInfos.objects(id=profile_id).first()


@router.post("/linkedin", response_model=ProfileInfoResponse)
def create_profile_from_linkedin_url(
    linkedinUrl: str,
    profileType: ProfileTypes,
    hubspotInfo: HubspotInfo | None = None,
    productInfo: ProductInfo | None = None,
):
    try:
        response, summary, buyingStyleInfo = linkedin_summary_generation(linkedinUrl)
        linkedIN_data = LinkedInInfos(
            url=str(linkedinUrl), data=response, summary=summary,buyingStyle=buyingStyleInfo
        )
        profile = ProfileInfos(
            profileType=profileType,
            profileId=str(ObjectId()),
            hubspotInfo=hubspotInfo,
            productInfo=productInfo,
            linkedinInfo=linkedIN_data,
        )
        profile = profile.save()
        return ProfileInfo(**profile.to_mongo(use_db_field=False))
    except Exception as e:
        handle_error(e)


@router.patch("/linkedin", response_model=ProfileInfoResponse)
def patch_profile_linkedin(
    linkedIN_data: LinkedInInfo, profile_id: str = Depends(valid_profile_id)
) -> bool:
    try:
        profile = get_profile(profile_id)
        linkedinInfo = LinkedInInfos(
            url=linkedIN_data.url,
            data=linkedIN_data.data,
            summary=linkedIN_data.summary,
            buyingStyle = linkedIN_data.buyingStyle
        )
        profile.update(linkedinInfo=linkedinInfo)
        profile.update(updatedAt=datetime.now())
        return True
    except Exception as e:
        handle_error(e)
        return False


@router.get("/{profile_id}", response_model=ProfileInfoResponse)
def read_profile(profile_id: str = Depends(valid_profile_id)):
    try:
        profile = get_profile(profile_id)
        return ProfileInfoResponse(**profile.to_mongo(use_db_field=False))
    except Exception as e:
        handle_error(e)


@router.post("/{profile_id}", response_model=ProfileInfoResponse)
def create_profile(profile_in: ProfileInfo):
    try:
        profile = ProfileInfos(
            profileType=profile_in.profileType,
            profileId=profile_in.profileId,
            productInfo=profile_in.productInfo,
            linkedinInfo=profile_in.linkedinInfo,
        )
        profile = profile.save()
        return ProfileInfoResponse(**profile.to_mongo(use_db_field=False))
    except Exception as e:
        handle_error(e)


@router.put("/{profile_id}", response_model=ProfileInfoResponse)
def update_profile(
    new_profile: ProfileInfo, profile_id: str = Depends(valid_profile_id)
):
    try:
        profile = get_profile(profile_id)
        profile_update_status = profile.modify(
            updatedAt=datetime.now(),
            profileType=new_profile.profileType,
            profileId=new_profile.profileId,
            productInfo=new_profile.productInfo,
            linkedinInfo=new_profile.linkedinInfo,
        )
        profile.reload()
        if profile_update_status:
            return ProfileInfoResponse(**profile.to_mongo(use_db_field=False))
        else:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="Unable to Update Transcript",
            )

    except Exception as e:
        handle_error(e)


@router.delete("/{profile_id}")
def delete_profile(profile_id: str = Depends(valid_profile_id)):
    try:
        profile = get_profile(profile_id)
        profile.delete()
        return {"message": "success"}
    except Exception as e:
        handle_error(e)
