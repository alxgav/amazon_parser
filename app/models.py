from pydantic import BaseModel
from typing import Optional

from pydantic import validator

class Book(BaseModel):
    title: str
    author: str
    rating: Optional[float] = None
    type_of_book: str
    price: float
    url: str

    @validator('rating', pre=True)
    def validate_rating(cls, value: Optional[float]) -> Optional[float]:
        if not value:
            return 
        if 0 <= value <= 5:
            return float(value)
        raise ValueError('Rating must be in [0, 5].')

    @validator('price', pre=True)
    def price_riplace(cls, a: str) -> float:
        return float(a.replace('$', '').strip())