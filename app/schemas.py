from collections import defaultdict

from typing import List
from pydantic import BaseModel


class ImageIn(BaseModel):
    image: str


class ImageOut(ImageIn):
    uuid: str
    is_negative: bool

    class Config:
        orm_mode = True


class ImagePair(BaseModel):
    uuid: str
    image: str
    neg_image: str


def get_pairs(images: List[ImageOut]) -> List[ImagePair]:
    pairs = []
    img_dict = defaultdict(dict)

    for img in images:
        img_dict[img.uuid]['neg_image' if img.is_negative else 'image'] = img.image

    for k, v in img_dict.items():
        pairs.append(ImagePair(**v, uuid=k))

    return pairs
