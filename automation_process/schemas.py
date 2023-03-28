from pydantic import BaseModel
import datetime as dt
from typing import List

class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str

    #items: list[User] = []

    class Config:
        orm_mode = True

class Response_user(BaseModel):
    response: List[User]

class Scan(BaseModel):
    id: int
    scann: str
    type_scan: str
    size: float
    unit_s: str
    weight: int
    unit_w: str
    owner_id: int
    date_created: dt.datetime
    
    class Config:
        orm_mode = True

class Response_scan(BaseModel):
    response: List[Scan]

class Insole(BaseModel):
    id: int
    data: str
    data_gcode: str
    data_stl: str

    class Config:
        orm_mode = True

class Response_insole(BaseModel):
    response: List[Insole]

