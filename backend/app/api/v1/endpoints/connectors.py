from fastapi import APIRouter, HTTPException, status

router = APIRouter()

# Phase 2: OAuth connect/disconnect + status for Gmail, Google Calendar, Google
# Drive, Outlook Calendar, Notion, Slack. WhatsApp/Apple Notes are deferred (see
# ARCHITECTURE.md) until the official-API connectors are working end to end.


@router.get("/", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def list_connectors() -> None:
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Connectors not implemented yet")
