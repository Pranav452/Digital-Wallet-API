#this file contains the routers for the user management system

from fastapi import APIRouter
from app.crud.User_Management import get_user, update_user

router = APIRouter()

router.get("/users/{user_id}")(get_user)
router.put("/users/{user_id}")(update_user)