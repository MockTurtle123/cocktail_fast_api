from fastapi import FastAPI, Depends, HTTPException

import crud
from database import engine, get_db
import models
import schemas
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title='CocktailFull Database API',
    description='Create, Read, Update and Delete Cocktails',
)


@app.get('/')
def home():
    return "Welcome to CocktailFull Database FAST-API. Go to /docs for more information."


@app.get("/cocktails/", response_model=list[schemas.CocktailShort])
def get_all_cocktails(db: Session = Depends(get_db)):
    """Return a list of all cocktails in the database. Schema: id, name"""
    cocktails = crud.get_list_of_cocktails(db)
    return cocktails


@app.get("/cocktail/id/{cocktail_id}", response_model=schemas.CocktailFull)
def get_cocktail_by_id(cocktail_id: int, db: Session = Depends(get_db)):
    """Return a cocktail with specified id. Schema: id, name, glass, garnish, preparation, ingredients"""
    db_cocktail = crud.get_cocktail_by_id(db, cocktail_id=cocktail_id)
    if db_cocktail is None:
        raise HTTPException(status_code=404, detail="CocktailFull not found")
    return db_cocktail


@app.get("/cocktail/name/{cocktail_name}", response_model=schemas.CocktailFull)
def get_cocktail_by_name(cocktail_name: str, db: Session = Depends(get_db)):
    """Return a cocktail with specified name. Schema: id, name, glass, garnish, preparation, ingredients"""
    db_cocktail = crud.get_cocktail_by_name(db, cocktail_name=cocktail_name)
    if not db_cocktail:
        raise HTTPException(status_code=404, detail="CocktailFull not found")
    return db_cocktail


@app.get('/ingredient/{ingredient_name}', response_model=list[schemas.CocktailShort])
def get_cocktails_by_ingredient_name(ingredient_name: str, db: Session = Depends(get_db)):
    """Return a list of cocktails containing specified ingredient. Schema: id, name"""
    db_cocktails = crud.get_cocktail_by_ingredient_name(db, ingredient_name)
    if not db_cocktails:
        raise HTTPException(status_code=404, detail=f"No cocktails with ingredient {ingredient_name} found")
    return db_cocktails


@app.post('/cocktails/')
def batch_create_cocktails(cocktails: list[schemas.CocktailBase], db: Session = Depends(get_db)):
    """Create cocktails by passing a list. (or create a single item py passing a list with a single item)
    Schema: id, name, glass, garnish, preparation, ingredients"""
    created_cocktails = crud.batch_create_cocktails(db, cocktails)
    return {"message": f'{len(created_cocktails)} cocktails created successfully!'}


@app.delete('/cocktail/id/{cocktail_id}')
def delete_cocktail(cocktail_id: int, db: Session = Depends(get_db)):
    """Delete cocktail with specified id."""
    return crud.delete_cocktail(db, cocktail_id)


@app.put('/cocktail/{cocktail_id}')
def update_cocktail(cocktail_id: int, cocktail_data: schemas.CocktailBase, db: Session = Depends(get_db)):
    """Update every field in the cocktail with specified id."""
    return crud.update_cocktail(db, cocktail_id, cocktail_data)


@app.patch('/cocktail/{cocktail_id}')
def patch_cocktail(cocktail_id: int, cocktail_data: schemas.CocktailBase, db: Session = Depends(get_db)):
    """Update selected fields in the cocktail with specified id."""
    return crud.patch_cocktail(db, cocktail_id, cocktail_data)

