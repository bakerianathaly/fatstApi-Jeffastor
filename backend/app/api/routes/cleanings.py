from typing import List
from fastapi import APIRouter, Body, Depends  
from starlette.status import HTTP_201_CREATED
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

@router.get('/cleaning/{name}', response_model=List[CleaningPublic], name = 'cleaning:get-all-cleaning-by-name',status_code = HTTP_201_CREATED)
async def get_cleaning_name(name: str, cleanings_repo: CleaningsRepository = Depends(get_repository(CleaningsRepository))) -> List[CleaningPublic]:
    get_cleanings = await cleanings_repo.get_cleaning_by_name(search_name=name)
    return get_cleanings