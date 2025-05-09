from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import Profile
from schemas import Profile, ProfileCreate, ProfileUpdate
from database import get_db

router = APIRouter()

@router.post("/", response_model=Profile)
async def create_profile(profile: ProfileCreate, db: AsyncSession = Depends(get_db)):
    db_profile = Profile(**profile.model_dump())
    db.add(db_profile)
    await db.commit()
    await db.refresh(db_profile)
    return db_profile

@router.get("/{user_id}", response_model=Profile)
async def get_profile(user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profile).where(Profile.id == user_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/{user_id}", response_model=Profile)
async def update_profile(user_id: str, profile_update: ProfileUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profile).where(Profile.id == user_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    for key, value in profile_update.dict().items():
        setattr(profile, key, value)
    
    await db.commit()
    await db.refresh(profile)
    return profile
