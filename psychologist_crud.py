#Install libraries
from pydantic import BaseModel 
from fastapi import APIRouter
import json
from typing import Dict,List

#Create base model for Serene app user
class Psychologist(BaseModel):
    psychologist_id: int
    name: str
    qualifications: str
    specialty: str
    availability: List[int]

#Defines a router to group and organize the API endpoints
router = APIRouter()

#Opens json_data and stores data in psy_data
psy_filename="json_data/psychologist.json"

with open(psy_filename,"r") as read_file:
	psy_data = json.load(read_file)

@router.get('/')
async def get_all_psy(): 
	return psy_data['psychologist']

#Untuk specific psychologist
@router.get('/{psychologist_id}')
async def get_psy(psy_id : int): 
	psy_found = False
	for psy_itr in psy_data['user']: 
		if psy_itr['user_id'] == psy_id:
			psy_found = True
			return psy_itr
	if not psy_found: 
		return "Psychologist is not found!"    
	
@router.get('/find/')
async def check_psyname(psyname : str): 
	psy_found = False
	for psy_itr in psy_data['psychologist']: 
		if psy_itr['name'] == psyname:
			psy_found = True
			return psy_itr
	if not psy_found: 
		return None

#Belum diedit
@router.post('/')
async def create_psy(psy: Psychologist):
	psy_dict = dict(psy)
	for psy_itr in psy_data['psychologist']: 
		if psy_itr['psychologist_id'] == psy.id:
			return "User ID has to be unique!"
	psy_data['user'].append(psy_dict)
	with open(psy_filename, "w") as write_file: 
		json.dump(psy_data, write_file)
	return "Successfully added psychologist!"

@router.put('/')
async def update_psy(psy : Psychologist):
	psy_dict = dict(psy)
	psy_found = False 
	
    #Asumsi bisa terdapat 2 psikolog dengan nama sama
	for psy_idx, psy_itr in enumerate(psy_data['user']): 
		if psy_itr['psychologist_id'] == psy_dict['psychologist_id']: 
			psy_found = True
			psy_data['psychologist'][psy_idx] = psy_dict
			with open(psy_filename, "w") as write_file:
				json.dump(psy_data, write_file)
			return "Successfully updated psychologist with ID " + psy_dict['psychologist_id'] + " and name " + psy_dict['name']
	if not psy_found: 
		return "Psychologist not found!"

@router.delete("/{psychologist_id}")
async def delete_psy(psy_id : int): 
	psy_found = False
	for psy_idx, psy_itr in enumerate(psy_data['psychologist']): 
		if psy_itr['psy_id'] == psy_id:
			psy_found = True
			psy_data['psychologist'].pop(psy_idx)
			with open(psy_filename, "w") as write_file: 
				json.dump(psy_data, write_file)
			return "Successfully deleted psychologist!"
	if not psy_found: 
		return "Psychologist not found!"