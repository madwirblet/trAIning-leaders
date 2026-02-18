## API endpoint to ensure server is running

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health_check():
    return {"status": "ok"}