from pydantic import BaseModel
from typing import *
from models import Restaurant, Menu

class RestaurantCreate(BaseModel):
    name:str
    gst_number:Optional[str]
    location:str


class RestaurantList(BaseModel):
    restaurant_list:List[Restaurant]

class RestaurantUpdate(BaseModel):
    id:int
    name: Optional[str] = None
    gst_number: Optional[str] = None
    location: Optional[str] = None

class RestaurantMenuCreate(BaseModel):
    restaurant_id:int
    item_name:str
    item_price:str
    item_vareity:Optional[str]

class RestaurantMenuList(BaseModel):
    restaurant_menu_list:List[Menu]

class RestaurantMenuUpdate(BaseModel):
    restaurant_id:int
    id:int
    item_name:Optional[str] = None
    item_price:Optional[str] = None
    item_vareity:Optional[str] = None
