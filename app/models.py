from database import Base
from sqlalchemy import Column, Integer, UnicodeText, String, Boolean


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String)
    image = Column(UnicodeText)
    is_negative = Column(Boolean, default=False)

    def __str__(self):
        return f"ID: {self.id}, is_neg: {self.is_negative}, uuid: {self.uuid}"
