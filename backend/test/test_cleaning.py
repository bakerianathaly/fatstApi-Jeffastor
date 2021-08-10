import pytest
from httpx import AsyncClient
from databases import Database
from fastapi import FastAPI
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from app.models.cleaning import CleaningCreate, CleaningInDB
from app.db.repositories.cleaning import CleaningsRepository

# decorate all tests with @pytest.mark.asyncio
pytestmark = pytest.mark.asyncio  

@pytest.fixture
def new_cleaning():
  return CleaningCreate(
    name="test cleaning",
    description="test description",
    price=0.00,
    cleaning_type="spot_clean",
  )

@pytest.fixture
async def test_cleaning(db: Database) -> CleaningInDB:
  cleaning_repo = CleaningsRepository(db)
  new_cleaning = CleaningCreate(
    name="fake cleaning name",
    description="fake cleaning description",
    price=9.99,
    cleaning_type="spot_clean",
  )
  return await cleaning_repo.create_cleaning(new_cleaning=new_cleaning)
   
class TestCleaningsRoutes:
  async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
    res = await client.post(app.url_path_for("cleaning:create-cleaning"), json={})
    assert res.status_code != HTTP_404_NOT_FOUND

  async def test_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient) -> None:
    res = await client.post(app.url_path_for("cleaning:create-cleaning"), json={})
    assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY 

class TestCreateCleaning:
  async def test_valid_input_creates_cleaning(self, app: FastAPI, client: AsyncClient, new_cleaning: CleaningCreate) -> None:

    res = await client.post(app.url_path_for("cleaning:create-cleaning"), json={"new_cleaning": new_cleaning.dict()})
    assert res.status_code == HTTP_201_CREATED
    created_cleaning = CleaningCreate(**res.json())
    assert created_cleaning == new_cleaning
    return created_cleaning

  #El parametrize sirve para crear diferentes casos de prueba con cosas invalidas, crea un test por cada caso
  @pytest.mark.parametrize(
    "invalid_payload, status_code",
    (
      (None, 422),
      ({}, 422),
      ({"name": "test_name"}, 422),
      ({"price": 10.00}, 422),
      ({"name": "test_name", "description": "test"}, 422),
    ),
  )
  async def test_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient, invalid_payload: dict, status_code: int) -> None:
    res = await client.post(
      app.url_path_for("cleaning:create-cleaning"), json={"new_cleaning": invalid_payload}
    )
    assert res.status_code == status_code

class TestGetCleaning:
  async def test_valid_get_cleaning(self, app: FastAPI, client: AsyncClient) -> None:
    res = await client.get(app.url_path_for("cleaning:get-all-cleanings"))
    assert res.status_code == HTTP_200_OK
    cleaning = CleaningInDB(**res.json()[0])
    assert cleaning.id == 1

  async def test_valid_get_cleaning_by_name(self, app: FastAPI, client: AsyncClient, test_cleaning: CleaningCreate) -> None:

    res = await client.get(app.url_path_for("cleaning:get-all-cleaning-by-name", nameSearch = test_cleaning.name))
    assert res.status_code == HTTP_200_OK
    cleaning = CleaningInDB(**res.json()[0])
    assert cleaning.name == test_cleaning.name