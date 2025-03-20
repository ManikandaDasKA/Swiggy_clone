from fastapi import APIRouter, Depends
from restaurant.schemas import RestaurantCreate, RestaurantList, RestaurantUpdate, RestaurantMenuCreate, RestaurantMenuList, RestaurantMenuUpdate
from sqlmodel import Session, select
from models import Menu,Restaurant
from database import get_session
from typing import *
from sqlalchemy.sql.operators import ilike_op

app = APIRouter(prefix="")

@app.post("/restaurant/create")
def restaurant_create(restaurent_request:RestaurantCreate,session:Session=Depends(get_session)):
    restaurant = Restaurant(name = restaurent_request.name,gst_number=restaurent_request.gst_number,location=restaurent_request.location)
    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)
    return {"message":"restaurant create successfully","data":restaurant.model_dump(),"errorcode":0}



@app.post("/restaurant/list")
def get_restaurant_list(session:Session =Depends(get_session)):
  stmt= select(Restaurant)
  restaurant_list:List[Restaurant]=session.exec(stmt)
  restaurant_list_schema = RestaurantList(restaurant_list=restaurant_list)
  return{"message":"restaurant list successful",
        "data":restaurant_list_schema.model_dump(),
        "errorcode":0}



@app.post("/restaurant/filter")
def get_restaurant_filter(rest_id:  int, session:Session =Depends(get_session)):
  stmt= select(Restaurant).where(Restaurant.id == rest_id)
  restaurant:Optional[Restaurant]=session.exec(stmt).first()
  if restaurant:
    return{"message":"restaurant list successful",
        "data":restaurant.model_dump(),
        "errorcode":0}
  else:
      return{"message":"restaurant not fund",
        "data":{},
        "errorcode":1}




@app.get("/restaurant/search")
def restaurant_search(name:str,session:Session=Depends(get_session)):
   stmt = select(Restaurant).where(ilike_op(Restaurant.name,f'%{name}%'))
   rest_found:List[Restaurant] = session.exec(stmt).all()

   if len(rest_found)>0:
      rest_list = RestaurantList(restaurant_list=rest_found)
      
      return {"errorcode":0,"data":rest_list.model_dump(),"message":"success"}
   else:
      return {"errorcode":1,"data":{},"message":f"no restaurants found under {name}"}
   



@app.post("/restaurant/update")
def restaurant_update(update_data: RestaurantUpdate,session:Session=Depends(get_session)):
    stmt= select(Restaurant).where(Restaurant.id == update_data.id)
    restaurant:Optional[Restaurant]=session.exec(stmt).first()
    if restaurant:
        if update_data.name:
            restaurant.name = update_data.name
        if update_data.gst_number:
            restaurant.gst_number = update_data.gst_number
        if update_data.location:
            restaurant.location = update_data.location
        session.add(restaurant)
        session.commit()
        session.refresh(restaurant)
        return {"message": "restaurant updated successfully", "data": restaurant.model_dump(),"errorcode": 0 }
    else:
        return {"message": "restaurant not found", "data": {},"errorcode": 1}
    



@app.post("/restaurant/delete")
def get_restaurant_delete(id:  int, session:Session =Depends(get_session)):
  stmt= select(Restaurant).where(Restaurant.id == id)
  restaurant:Optional[Restaurant]=session.exec(stmt).first()
  if restaurant:
    session.delete(restaurant)
    session.commit()
    return{"message":"restaurant deleted successful",
        "errorcode":0}
  else:
      return{"message":"restaurant not fund",
        "errorcode":1}
  



@app.post("/restaurant/menu/create")
def restaurant_menu_create(restaurent_menu_request:RestaurantMenuCreate,session:Session=Depends(get_session)):
    restaurantmenu = Menu(restaurant_id=restaurent_menu_request.restaurant_id ,item_name = restaurent_menu_request.item_name,item_price=restaurent_menu_request.item_price,item_vareity=restaurent_menu_request.item_vareity)
    session.add(restaurantmenu)
    session.commit()
    session.refresh(restaurantmenu)
    return {"message":"restaurant menu create successfully","data":restaurantmenu.model_dump(),"errorcode":0}




@app.post("/restaurant/menu/list")
def get_restaurant_menu_list(session:Session = Depends(get_session)):
  stmt= select(Menu)
  restaurant_menu_list:List[Menu]=session.exec(stmt)
  restaurant_menu_list_schema = RestaurantMenuList(restaurant_menu_list=restaurant_menu_list)
  return{"message":"restaurant list successful",
        "data":restaurant_menu_list_schema.model_dump(),
        "errorcode":0}




@app.get("/restaurant/menu/search")
def restaurant_search(item_name:str,session:Session=Depends(get_session)):
   stmt = select(Menu).where(ilike_op(Menu.item_name,f'%{item_name}%'))
   menu_found:List[Menu] = session.exec(stmt).all()

   if len(menu_found)>0:
      menu_list = RestaurantMenuList(restaurant_menu_list=menu_found)
      
      return {"errorcode":0,"data":menu_list.model_dump(),"message":"success"}
   else:
      return {"errorcode":1,"data":{},"message":f"no restaurants found under {item_name}"}
   


@app.post("/restaurant/menu/update")
def restaurant_menu_update(update_menu_data: RestaurantMenuUpdate,session:Session=Depends(get_session)):
    stmt= select(Menu).where((Menu.restaurant_id == update_menu_data.restaurant_id) & (Menu.id == update_menu_data.id))
    menu:Optional[Menu]=session.exec(stmt).first()
    if menu:
        if update_menu_data.item_name:
            menu.item_name = update_menu_data.item_name
        if update_menu_data.item_price:
            menu.item_price= update_menu_data.item_price
        if update_menu_data.item_vareity:
            menu.item_vareity = update_menu_data.item_vareity
        session.add(menu)
        session.commit()
        session.refresh(menu)
        return {"message": "restaurant menu updated successfully", "data": menu.model_dump(),"errorcode": 0 }
    else:
        return {"message": "restaurant menu not found", "data": {},"errorcode": 1}




@app.post("/restaurant/menu/delete")
def get_restaurant_delete(restaurant_id: int, id:int, session:Session = Depends(get_session)):
  stmt= select(Menu).where((Menu.restaurant_id == restaurant_id) & (Menu.id == id))
  menu:Optional[Menu]=session.exec(stmt).first()
  if menu:
    session.delete(menu)
    session.commit()
    return{"message":"restaurant menu deleted successful",
        "errorcode":0}
  else:
      return{"message":"restaurant menu not fund",
        "errorcode":1}