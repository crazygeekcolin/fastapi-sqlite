from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base
from typing_extensions import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from datetime import datetime
import time


a = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
time.sleep(1)
b= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(a,b)


print(b>a)
print(datetime.now().date())

class User(BaseModel):
    id: int
    name: str = 'Jane Doe'

user = User(id='123')
assert user.id == 123
assert isinstance(user.id, int)



Base = declarative_base()


class CompanyOrm(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))


class CompanyModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    public_key: Annotated[str, StringConstraints(max_length=20)]
    name: Annotated[str, StringConstraints(max_length=63)]
    domains: List[Annotated[str, StringConstraints(max_length=255)]]


co_orm = CompanyOrm(
    id=123,
    public_key='foobar',
    name='Testing',
    domains=['example.com', 'foobar.com'],
)
print(co_orm)
co_model = CompanyModel.model_validate(co_orm)
print(co_model)

from typing import List

from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    list_of_ints: List[int]
    a_float: float


data = dict(
    list_of_ints=['1', 2, 'bad'],
    a_float='not a float',
)

try:
    Model(**data)
except ValidationError as e:
    print(e)
    
print(datetime(2013,2,25))

print(datetime(2013,2,25).date())

#Default value in pydantic
from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


def date_now() -> datetime:
    return datetime.now(timezone.utc).date()


class Model(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    updated: datetime = Field(default_factory=date_now)


m1 = Model()
m2 = Model()
assert m1.uid != m2.uid


print('ok',m1.uid ,m2.uid, type(m1.updated))


from pydantic import BaseModel, ValidationError


class Model(BaseModel):
    a: int
    b: int


# simply validating a dict
print(Model.model_validate({'a': 1, 'b': 2}))
#> a=1 b=2


class CustomObj:
    def __init__(self, a, b):
        self.a = a
        self.b = b


# using from attributes to extract fields from an objects
print(Model.model_validate(CustomObj(3, 4), from_attributes=True))
#> a=3 b=4


try:
    Model.model_validate('not an object', from_attributes=True)
except ValidationError as exc:
    print(repr(exc.errors()[0]['type']))
    print(exc)