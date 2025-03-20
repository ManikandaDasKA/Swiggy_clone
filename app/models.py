from  sqlmodel import SQLModel, Field
from typing import *

class Menu(SQLModel,table=True):
    id:Optional[int] = Field(primary_key=True,default=None)
    restaurant_id:int = Field(foreign_key="restaurant.id")
    item_name:str
    item_price:str
    item_vareity:Optional[str]

class Restaurant(SQLModel,table=True):
    id:Optional[int] = Field(primary_key=True,default=None)
    name:str
    gst_number:Optional[str]
    location:str
