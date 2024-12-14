from fastapi import APIRouter
from app.services.session_service import SessionService
from app.schemas.session_schemas import SessionResponse, SessionDetailsResponse

router = APIRouter()


@router.get("/session/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    """Retrieve a checkout session"""
    return await SessionService.get_session(session_id)


@router.get("/session/{session_id}/details", response_model=SessionDetailsResponse)
async def get_session_details(session_id: str):
    """Retrieve detailed information about a successful checkout session"""
    return await SessionService.get_session_details(session_id)
