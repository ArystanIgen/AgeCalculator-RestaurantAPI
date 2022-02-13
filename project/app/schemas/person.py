from pydantic import BaseModel, Field


class PersonIn(BaseModel):
    iin: str = Field(..., regex=r'^\d{12}$')


class PersonCreate(BaseModel):
    iin: str
    age: int


class PersonUpdate(BaseModel):
    iin: str
    age: int


class PersonOut(BaseModel):
    iin: str
    age: int

    class Config:
        orm_mode = True
