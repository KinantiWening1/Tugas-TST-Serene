#Install libraries
from fastapi import APIRouter, Depends, HTTPException
import json
from typing import Dict,List
from auth import oauth2_scheme, get_current_active_admin_user
from models import User
from update_passwords import get_password_hash

import certifi

ca = certifi.where()

from pymongo import MongoClient

client = MongoClient("mongodb+srv://asih_tst:Akiratst2021!@asihtst.hun0hrd.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client['serene_be']
collection = db['user']

user_data = collection.find_one()

def write_data(data):
    collection.replace_one({}, data, upsert=True)

#Defines a router to group and organize the API endpoints
router = APIRouter(tags=["user"])

#Opens json_data and stores data in user_data
#user_filename="json_data/user.json"

#with open(user_filename,"r") as read_file:
	#user_data = json.load(read_file)
	#print(user_data)

@router.get('/')
async def get_all_users(): 
	return user_data['user']

#Untuk specific user 
@router.get('/{user_id}')
async def get_user(user_id : int, cur_user: User = Depends(get_current_active_admin_user)): 
	user_found = False
	for user_itr in user_data['user']: 
		if user_itr['user_id'] == user_id:
			user_found = True
			return user_itr
	if not user_found: 
		return "User is not found!"    
	
@router.get('/find/')
async def check_username(username : str, cur_user: User = Depends(get_current_active_admin_user)): 
	user_found = False
	for user_itr in user_data['user']: 
		if user_itr['username'] == username:
			user_found = True
			return user_itr
	if not user_found: 
		return None

@router.post('/')
async def create_user(user: User):
    # Generate a new user ID
    user_id = max(u['user_id'] for u in user_data['user']) + 1

    # Set default values for disabled, tags, preferences and day
    user.disabled = False
    user.tags = "regular"

    # Hash the password
    user.hashed_password = get_password_hash(user.password)

	# User preference and day
    user.preference = "-"
    user.day = [0]
    
    # Create a dictionary from the user model
    user_dict = dict(user)

    # Check for uniqueness of username and user ID
    for user_itr in user_data['user']:
        if user_itr['username'] == user.username or user_itr['user_id'] == user_id:
            raise HTTPException(status_code=400, detail="Username and user IDs have to be unique!")

    # Set the user ID to the generated value
    user_dict['user_id'] = user_id
    
    # Append the user to the data
    user_data['user'].append(user_dict)
    
    # Update the user data file
    write_data(user_data)
    
    return {"message": "Successfully added user!", "user_id": user_id}

@router.put('/')
async def update_user(user: User, cur_user : User = Depends(get_current_active_admin_user)):
	user_dict = dict(user)
	user_found = False 
	for user_itr in user_data['user']: 
		if user_itr['username'] == user.username:
			return "Username already exists!"
	for user_idx, user_itr in enumerate(user_data['user']): 
		if user_itr['user_id'] == user_dict['user_id']: 
			user_found = True
			user_data['user'][user_idx] = user_dict
			write_data(user_data)
			return "Successfully updated user with username " + user_dict['username']
	if not user_found: 
		return "User not found!"

@router.delete("/{user_id}")
async def delete_user(user_id: int, user: User = Depends(get_current_active_admin_user)):
	user_found = False
	for user_idx, user_itr in enumerate(user_data['user']): 
		if user_itr['user_id'] == user_id:
			user_found = True
			user_data['user'].pop(user_idx)
			write_data(user_data)
			return "Successfully deleted user"
	if not user_found: 
		return "User not found!"