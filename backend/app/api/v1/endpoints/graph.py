from fastapi import APIRouter, HTTPException, status

router = APIRouter()

# Phase 2/3: entity extraction populates node/edge tables during ingestion;
# this endpoint will serve them to replace graph.html's hardcoded dataset.


@router.get("/", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def get_graph() -> None:
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Graph not implemented yet")
