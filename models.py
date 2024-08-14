from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

from database import Base


class Cocktail(Base):
    __tablename__ = 'cocktails'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    glass = Column(String)
    garnish = Column(String)
    preparation = Column(String)

    ingredients = relationship('Ingredient', back_populates="cocktail")


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True, index=True)
    ingredient = Column(String)
    label = Column(String)
    amount = Column(Float)
    unit = Column(String)
    special = Column(String)
    cocktail_id = Column(Integer, ForeignKey("cocktails.id"))

    cocktail = relationship('Cocktail', back_populates='ingredients')



