from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


""" class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))

    @hybrid_property
    def fullname(self):
        return self.firstname + " " + self.lastname

some_user = session.query(User).first()
print(some_user.fullname)
print('ok') """

from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    x: str


try:
    Model()
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    print(exc)
    #> 'missing'