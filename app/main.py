import uuid

import uvicorn
from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

import crud
import models
from schemas import ImageIn, ImageOut, ImagePair, get_pairs
from database import SessionLocal, engine
from image_modifier import ImageModifier


# Create DB tables
models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.mount("/static", StaticFiles(directory='frontend/static'), name='static')


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def index_page():
    with open('frontend/index.html', encoding='utf-8') as file:
        html_content = ''.join(file.readlines())
    return HTMLResponse(content=html_content)


@app.get('/view_images')
async def view_images_page():
    with open('frontend/view_images.html', encoding='utf-8') as file:
        html_content = ''.join(file.readlines())
    return HTMLResponse(content=html_content)


@app.post('/negative_image', response_model=ImageOut)
async def negative_image(image: ImageIn, db: Session = Depends(get_db)):
    uuid_ = uuid.uuid1()
    crud.create_image(db=db, image=image, is_negative=False, uuid_=uuid_)

    inverted = ImageModifier(image.image).inverted_img
    return crud.create_image(db=db, image=ImageIn(image=inverted), is_negative=True, uuid_=uuid_)


@app.get('/get_last_images', response_model=List[ImagePair])
async def get_last_images(db: Session = Depends(get_db)):
    images = crud.get_last_pair_images(db, 3)
    return get_pairs(images)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
