import uuid

from sqlalchemy import desc
from sqlalchemy.orm import Session

import schemas
from models import Image


def create_image(db: Session, image: schemas.ImageIn, is_negative=False, uuid_=None):
    db_image = Image(image=image.image, is_negative=is_negative, uuid=uuid_ or uuid.uuid1())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    return db_image


def get_last_pair_images(db: Session, count: int):
    uuids = db.query(Image.uuid) \
        .filter(Image.is_negative) \
        .order_by(desc(Image.id))\
        .limit(count)

    imgs = db.query(Image).filter(Image.uuid.in_(uuids))
    return imgs.all()
