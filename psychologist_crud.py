#Install libraries
from fastapi import APIRouter, Depends, HTTPException
import json
from typing import Dict,List
from auth import oauth2_scheme, get_current_active_user, get_current_active_admin_user
from models import Psychologist, User
import certifi

ca = certifi.where()

from pymongo import MongoClient

client = MongoClient("mongodb+srv://asih_tst:Akiratst2021!@asihtst.hun0hrd.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client['serene_be']
collection = db['psychologist']

psy_data = collection.find_one()

def write_data(data):
    collection.replace_one({}, data, upsert=True)

#Defines a router to group and organize the API endpoints
router = APIRouter()

#Opens json_data and stores data in psy_data
# psy_filename="json_data/psychologist.json"

# with open(psy_filename,"r") as read_file:
# psy_data = json.load(read_file)

@router.get('/')
async def get_all_psy(user: User = Depends(get_current_active_user)): 
	return psy_data['psychologist']

#Untuk specific psychologist
@router.get('/{psychologist_id}')
async def get_psy(psy_id : int, user: User = Depends(get_current_active_user)): 
	psy_found = False
	for psy_itr in psy_data['user']: 
		if psy_itr['user_id'] == psy_id:
			psy_found = True
			return psy_itr
	if not psy_found: 
		return "Psychologist is not found!"    
	
@router.get('/find/')
async def check_psyname(psyname : str, user: User = Depends(get_current_active_user)): 
	psy_found = False
	for psy_itr in psy_data['psychologist']: 
		if psy_itr['name'] == psyname:
			psy_found = True
			return psy_itr
	if not psy_found: 
		return None

@router.post('/')
async def create_psy(psy: Psychologist, cur_user: User = Depends(get_current_active_admin_user)):
	psy_dict = dict(psy)
	for psy_itr in psy_data['psychologist']: 
		if psy_itr['psychologist_id'] == psy.psychologist_id:
			return "Psychologist ID has to be unique!"
	psy_data['psychologist'].append(psy_dict)
	write_data(psy_data)
	return "Successfully added psychologist!"

@router.put('/')
async def update_psy(psy : Psychologist, cur_user: User = Depends(get_current_active_admin_user)):
	psy_dict = dict(psy)
	psy_found = False 
	
    #Asumsi bisa terdapat 2 psikolog dengan nama sama
	for psy_idx, psy_itr in enumerate(psy_data['user']): 
		if psy_itr['psychologist_id'] == psy_dict['psychologist_id']: 
			psy_found = True
			psy_data['psychologist'][psy_idx] = psy_dict
			write_data(psy_data)
			return "Successfully updated psychologist with ID " + psy_dict['psychologist_id'] + " and name " + psy_dict['name']
	if not psy_found: 
		return "Psychologist not found!"

@router.delete("/{psychologist_id}")
async def delete_psy(psy_id : int, cur_user: User = Depends(get_current_active_admin_user)): 
	psy_found = False
	for psy_idx, psy_itr in enumerate(psy_data['psychologist']): 
		if psy_itr['psychologist_id'] == psy_id:
			psy_found = True
			psy_data['psychologist'].pop(psy_idx)
			write_data(psy_data)
			return "Successfully deleted psychologist!"
	if not psy_found: 
		return "Psychologist not found!"