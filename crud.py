from sqlalchemy.orm import Session
from fastapi import HTTPException
import models
import schemas


# GET requests


def get_list_of_cocktails(db: Session):
    return db.query(models.Cocktail).all()


def get_cocktail_by_id(db: Session, cocktail_id: int):
    return db.query(models.Cocktail).filter(models.Cocktail.id == cocktail_id).first()  # type: ignore


def get_cocktail_by_name(db: Session, cocktail_name: str):
    name_title = cocktail_name.title()
    return db.query(models.Cocktail).filter(models.Cocktail.name == name_title).first()  # type: ignore


def get_cocktail_by_ingredient_name(db: Session, ingredient_name: str):
    name_title = ingredient_name.title()
    cocktails = (
        db.query(models.Cocktail)
        .join(models.Cocktail.ingredients)
        .filter(models.Ingredient.ingredient == name_title)  # type: ignore
        .all()
    )
    return cocktails


# POST requests

def batch_create_cocktails(db: Session, cocktails: list[schemas.CocktailBase]):
    created_cocktails = []
    for cocktail in cocktails:
        db_cocktail = models.Cocktail(
            name=cocktail.name,
            glass=cocktail.glass,
            garnish=cocktail.garnish,
            preparation=cocktail.preparation
        )
        db.add(db_cocktail)
        db.commit()
        db.refresh(db_cocktail)

        for ingredient in cocktail.ingredients:
            db_ingredient = models.Ingredient(
                cocktail_id=db_cocktail.id,
                unit=ingredient.unit,
                amount=ingredient.amount,
                ingredient=ingredient.ingredient,
                label=ingredient.label,
                special=ingredient.special
            )
            db.add(db_ingredient)

        db.commit()
        created_cocktails.append(db_cocktail)
    return created_cocktails


# DELETE requests

def delete_cocktail(db: Session, cocktail_id: int):
    db_cocktail = db.get(models.Cocktail, cocktail_id)
    if not db_cocktail:
        raise HTTPException(status_code=404, detail=f'CocktailFull (id={cocktail_id}) not found')
    db.delete(db_cocktail)
    db.commit()
    return {'message': f'CocktailFull (id={cocktail_id}) deleted successfully'}


# PUT requests

def update_cocktail(db: Session, cocktail_id: int, cocktail_data: schemas.CocktailUpdate):
    db_cocktail = db.get(models.Cocktail, cocktail_id)
    if not db_cocktail:
        raise HTTPException(status_code=404, detail=f'CocktailFull (id={cocktail_id}) not found')

    db_cocktail.name = cocktail_data.name
    db_cocktail.glass = cocktail_data.glass
    db_cocktail.garnish = cocktail_data.garnish
    db_cocktail.preparation = cocktail_data.preparation

    for ingredient in cocktail_data.ingredients:
        db_ingredient = models.Ingredient(
            cocktail_id=db_cocktail.id,  # type: ignore
            unit=ingredient.unit,
            amount=ingredient.amount,
            ingredient=ingredient.ingredient,
            label=ingredient.label,
            special=ingredient.special
        )
        db.add(db_ingredient)

    db.commit()
    db.refresh(db_cocktail)

    return {'message': f"Cocktail id={cocktail_id} updated successfully",
            "new info": db_cocktail}

# PATCH requests

# def patch_cocktail(db: Session, cocktail_id: int, cocktail: schemas.CocktailBase):
#     db_cocktail = db.get(models.Cocktail, cocktail_id)
#     if not db_cocktail:
#         raise HTTPException(status_code=404, detail=f'CocktailFull (id={cocktail_id}) not found')
#     if cocktail.glass:
#         db_cocktail.glass = cocktail.glass
#     if cocktail.glass:
#         db_cocktail.glass = cocktail.glass
