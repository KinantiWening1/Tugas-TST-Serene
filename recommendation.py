from fastapi import APIRouter, Depends, HTTPException
import json
from typing import Dict,List
from auth import oauth2_scheme, get_current_active_admin_user, get_current_active_user
from models import User
import integration

#Defines a router to group and organize the API endpoints
router = APIRouter()

@router.get('/{mood}/{amount}')
async def get_recommendation(mood : str, amount : int): 
	return integration.get_movie_recommendation(mood, amount)