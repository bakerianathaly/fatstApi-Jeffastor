from os import name
from typing import Optional, List
from enum import Enum
from app.models.core import IDModelMixin, CoreModel
from pydantic import Field

class CleaningType(str, Enum):
    dust_up = "dust_up"
    spot_clean = "spot_clean"
    full_clean = "full_clean"

class CleaningBase(CoreModel):
    """
    All common characteristics of our Cleaning resource
    """
    name: str = Field(..., min_length = 2)
    description: Optional[str]
    price: float = Field(..., gt= 5.0)
    cleaning_type: CleaningType = "spot_clean"

class CleaningCreate(CleaningBase):
    name: str
    price: float

class CleaningUpdate(CleaningBase):
    cleaning_type: Optional[CleaningType]
    price: Optional[float]

class CleaningInDB(IDModelMixin, CleaningBase):
    name: str
    price: float
    cleaning_type: CleaningType

class CleaningPublic(IDModelMixin, CleaningBase):
    name: str
    price: float
    cleaning_type: CleaningType
    description: Optional[str]