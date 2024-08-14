from enum import Enum
from pydantic import BaseModel


class Glass(str, Enum):
    OLD_FASHIONED = 'old-fashioned'
    MARTINI = 'martini'
    COLLINS = 'collins'
    HIGHBALL = 'highball'
    CHAMPAGNE_FLUTE = 'champagne-flute'
    MARGARITA = 'margarita'
    CHAMPAGNE_TULIP = 'champagne-tulip'
    HURRICANE = 'hurricane'
    SHOT = 'shot'
    HOT_DRINK = 'hot-drink'
    WHITE_WINE = 'white-wine'


class Ingredient(BaseModel):

    ingredient: str | None = None
    label: str | None = None
    amount: int | float | None = None
    unit: str | None = None
    special: str | None = None

    class Config:
        orm_mode = True


class CocktailBase(BaseModel):

    name: str
    glass: Glass
    garnish: str | None = None
    preparation: str | None = None
    ingredients: list[Ingredient] | None = None

    class Config:
        orm_mode = True


class CocktailFull(CocktailBase):

    id: int

    class Config:
        orm_mode = True


class CocktailShort(BaseModel):
    id: int
    name: str

