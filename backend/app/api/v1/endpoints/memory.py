from fastapi import APIRouter, HTTPException, status

router = APIRouter()

# Phase 2/4: memory search, timeline listing, and category-filtered aggregation
# (e.g. "list all my certifications") land here.


@router.get("/search", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def search_memory() -> None:
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Memory search not implemented yet")
