from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_200_OK,HTTP_404_NOT_FOUND
from app.models.cleaning import CleaningCreate, CleaningPublic  
from app.db.repositories.cleaning import CleaningsRepository  
from app.api.dependencies.database import get_repository  

router = APIRouter()

@router.get("/")
async def get_all_cleanings() -> List[dict]:
    cleanings = [
        {"id": 1, "name": "My house", "cleaning_type": "full_clean", "price": 29.99},
        {"id": 2, "name": "Someone else's house", "cleaning_type": "spot_clean", "price": 19.99}
    ]
    return cleanings

@router.post("/", response_model=CleaningPublic, name="cleaning:create-cleaning", status_code=HTTP_201_CREATED)
async def create_new_cleaning(
        new_cleaning: CleaningCreate = Body(..., embed=True),
        cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository)),
    ) -> CleaningPublic:
    created_cleaning = await cleanings_repo.create_cleaning(new_cleaning=new_cleaning)
    return created_cleaning

@router.get('/cleaning/{nameSearch}', response_model=List[CleaningPublic], name = 'cleaning:get-all-cleaning-by-name',status_code = HTTP_200_OK)
async def get_cleaning_name(nameSearch: str, cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository))) -> List[CleaningPublic]:
    get_cleanings = await cleanings_repo.get_cleaning_by_name(search_name = nameSearch)
    if not get_cleanings:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No cleaning found with that name.")

    return get_cleanings

@router.get('/all/cleaning/', response_model=List[CleaningPublic], name ='cleaning:get-all-cleanings', status_code = HTTP_200_OK)
async def get_all_cleaning(cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository))) -> List[CleaningPublic]:
    all_cleaning = await cleanings_repo.get_all_cleaning()
    
    if not all_cleaning:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No cleaning found.")

    return all_cleaning 