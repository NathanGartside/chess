from fastapi import APIRouter

router = APIRouter()


@router.get("/get-message")
async def read_root():
    return {"Message": "Congrats! This is your first api!"}
