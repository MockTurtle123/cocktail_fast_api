from fastapi import FastAPI, Depends, HTTPException

import crud
from database import SessionLocal, engine
import models
import schemas
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    title='Cocktail Database API',
    description='Create, Read, Update and Delete Cocktails',
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def home():
    return "Welcome to Cocktail Database FAST-API"


@app.get("/cocktails/", response_model=list[schemas.Cocktail])
def get_all_cocktails(db: Session = Depends(get_db)):
    cocktails = crud.get_list_of_cocktails(db)
    return cocktails


@app.get("/cocktail/id/{cocktail_id}", response_model=schemas.Cocktail)
def get_cocktail_by_id(cocktail_id: int, db: Session = Depends(get_db)):
    db_cocktail = crud.get_cocktail_by_id(db, cocktail_id=cocktail_id)
    if db_cocktail is None:
        raise HTTPException(status_code=404, detail="Cocktail not found")
    return db_cocktail


@app.get("/cocktail/name/{cocktail_name}", response_model=schemas.Cocktail)
def get_cocktail_by_name(cocktail_name: str, db: Session = Depends(get_db)):
    db_cocktail = crud.get_cocktail_by_name(db, cocktail_name=cocktail_name)
    if not db_cocktail:
        raise HTTPException(status_code=404, detail="Cocktail not found")
    return db_cocktail


@app.get('/ingredient/{ingredient_name}', response_model=list[schemas.Cocktail])
def get_cocktails_by_ingredient_name(ingredient_name: str, db: Session = Depends(get_db)):
    db_cocktails = crud.get_cocktail_by_ingredient_name(db, ingredient_name)
    if not db_cocktails:
        raise HTTPException(status_code=404, detail=f"No cocktails with ingredient {ingredient_name} found")
    return db_cocktails


@app.post('/cocktails/')
def batch_create_cocktails(cocktails: list[schemas.Cocktail], db: Session = Depends(get_db)):
    created_cocktails = crud.batch_create_cocktails(db, cocktails)
    return {"message": f'{len(created_cocktails)} cocktails created successfully!'}


@app.delete('/cocktail/id/{cocktail_id}')
def delete_cocktail(cocktail_id: int, db: Session = Depends(get_db)):
    crud.delete_cocktail(db, cocktail_id)