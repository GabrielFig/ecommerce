from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.crud.user import create_user, get_user, update_user, delete_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead)
async def create_new_user(user: UserCreate):
    db_user = await create_user(user)
    if not db_user:
        raise HTTPException(status_code=400, detail="User could not be created")
    return db_user

@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int):
    db_user = await get_user(user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=UserRead)
async def update_existing_user(user_id: int, user: UserUpdate):
    db_user = await update_user(user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=dict)
async def delete_existing_user(user_id: int):
    result = await delete_user(user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}