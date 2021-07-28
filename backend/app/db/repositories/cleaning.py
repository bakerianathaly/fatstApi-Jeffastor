#Con los repositorios desacoplamos la lógica de persistencia de nuestra lógica de aplicación

from app.db.repositories.base import BaseRepository
from app.models.cleaning import CleaningCreate, CleaningUpdate, CleaningInDB, CleaningPublic
from typing import List 

INSERT_CLEANING_QUERY = """
    INSERT INTO cleaning (name, description, price, cleaning_type)
    VALUES (:name, :description, :price, :cleaning_type)
    RETURNING id, name, description, price, cleaning_type;
"""

QUERY_CLEANING_BY_NAME = """
    SELECT *
    FROM cleaning
    WHERE name = :search_name
"""

class CleaningsRepository(BaseRepository):
    """"
    All database actions associated with the Cleaning resource
    """
    async def create_cleaning(self, *, new_cleaning: CleaningCreate) -> CleaningInDB:
        print('valor antes de ser JSON: ', new_cleaning)
        query_values = new_cleaning.dict()
        cleaning = await self.db.fetch_one(query=INSERT_CLEANING_QUERY, values=query_values)
        return CleaningInDB(**cleaning)

    async def get_cleaning_by_name(self, *, search_name: str) -> List[CleaningPublic]:
        search_name = {'search_name':search_name}
        cleaning = await self.db.fetch_all(query=QUERY_CLEANING_BY_NAME, values=search_name)
        
        return cleaning
