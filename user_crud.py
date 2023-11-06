#Install libraries
from pydantic import BaseModel 
from fastapi import APIRouter
import json
from typing import Dict,List

#Create base model for Serene app user
class User(BaseModel):
	user_id: int
	username: str
	email: str
	password: str
	date_of_birth: str
	gender: str
	day: List[int]  # Indentation should be consistent
	preference: str  # Indentation should be consistent

#Defines a router to group and organize the API endpoints
router = APIRouter()

#Opens json_data and stores data in user_data
user_filename="json_data/user.json"

with open(user_filename,"r") as read_file:
	user_data = json.load(read_file)
	print(user_data)

@router.get('/')
async def get_all_users(): 
	return user_data['user']

#Untuk specific user 
@router.get('/{user_id}')
async def get_user(user_id : int): 
	user_found = False
	for user_itr in user_data['user']: 
		if user_itr['user_id'] == user_id:
			user_found = True
			return user_itr
	if not user_found: 
		return "User is not found!"    
	
@router.get('/find/')
async def check_username(username : str): 
	user_found = False
	for user_itr in user_data['user']: 
		if user_itr['username'] == username:
			user_found = True
			return user_itr
	if not user_found: 
		return None

#Belum diedit
@router.post('/')
async def create_user(user: User):
	user_dict = dict(user)
	for user_itr in user_data['user']: 
		if user_itr['username'] == user.username or user_itr['user_id'] == user.id:
			return "Username and user IDs has to be unique!"
	user_data['user'].append(user_dict)
	with open(user_filename, "w") as write_file: 
		json.dump(user_data, write_file)
	return "Successfully added user!"

@router.put('/')
async def update_user(user : User):
	user_dict = dict(user)
	user_found = False 
	for user_itr in user_data['user']: 
		if user_itr['username'] == user.username:
			return "Username already exists!"
	for user_idx, user_itr in enumerate(user_data['user']): 
		if user_itr['user_id'] == user_dict['user_id']: 
			user_found = True
			user_data['user'][user_idx] = user_dict
			with open(user_filename, "w") as write_file:
				json.dump(user_data, write_file)
			return "Successfully updated user with username " + user_dict['username']
	if not user_found: 
		return "User not found!"

@router.delete("/{user_id}")
async def delete_user(user_id : int): 
	user_found = False
	for user_idx, user_itr in enumerate(user_data['user']): 
		if user_itr['user_id'] == user_id:
			user_found = True
			user_data['user'].pop(user_idx)
			with open(user_filename, "w") as write_file: 
				json.dump(user_data, write_file)
			return "Successfully deleted user"
	if not user_found: 
		return "User not found!"