from fastapi import APIRouter, HTTPException, status

router = APIRouter()

# Phase 4: RAG chat (retrieve + Claude synthesis with citations).
# Phase 5: agentic tool-use loop for actions (e.g. send_email), always gated
# behind a user-confirmation step before anything irreversible executes.


@router.post("/", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def send_message() -> None:
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Chat not implemented yet")
