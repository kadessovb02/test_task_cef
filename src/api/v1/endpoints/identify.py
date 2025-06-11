from fastapi import APIRouter, UploadFile, File, Depends

from src.services.face_service import face_service
from src.models.schemas.identify import IdentifyResponse
from src.api.v1.deps import require_auth

router = APIRouter(tags=["face"])

@router.post("/identify", response_model=IdentifyResponse)
async def identify(file: UploadFile = File(...), user = Depends(require_auth)):
    return await face_service.identify_face(file)
