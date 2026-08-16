from fastapi import APIRouter, HTTPException, status

router = APIRouter()

# Phase 2: real signup/login (password hashing, JWT issuance) lands here.


@router.post("/signup", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def signup() -> None:
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Auth not implemented yet")


@router.post("/login", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def login() -> None:
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, "Auth not implemented yet")
