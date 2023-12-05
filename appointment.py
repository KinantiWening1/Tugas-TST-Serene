#Install libraries
from fastapi import APIRouter, Depends, HTTPException, status
import json
from typing import Dict,List
from auth import oauth2_scheme, get_current_active_user, get_current_active_admin_user
from models import Appointment,User,Psychologist
import certifi

ca = certifi.where()

from pymongo import MongoClient

client = MongoClient("mongodb+srv://asih_tst:Akiratst2021!@asihtst.hun0hrd.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)
db = client['serene_be']
collection = db['appointment']
collection_user = db['user']
collection_psy = db['psychologist']

app_data = collection.find_one()
user_data = collection_user.find_one()
psy_data = collection_psy.find_one()

def write_data(data):
    collection.replace_one({}, data, upsert=True)

#Defines a router to group and organize the API endpoints
router = APIRouter()

#Opens json_data and stores data in app_data
# app_filename="json_data/appointment.json"

# with open(app_filename,"r") as read_file:
# app_data = json.load(read_file)

@router.get('/')
async def get_all_app(cur_user: User = Depends(get_current_active_user)): 
	return app_data['appointment']

#Untuk specific appointment
@router.get('/{appointment_id}')
async def get_app(app_id : int, user: User = Depends(get_current_active_user)): 
	app_found = False
	for app_itr in app_data['user']: 
		if app_itr['app_id'] == app_id:
			app_found = True
			return app_itr
	if not app_found: 
		return "Appointment is not found!"    

@router.post('/')
async def create_app(app: Appointment, cur_user: User = Depends(get_current_active_admin_user)):
    app_dict = dict(app)

    # Check if user_id exists
    user_exists = False
    for user_itr in user_data['user']: 
        if user_itr['user_id'] == app_dict['user_id']:
            user_exists = True
    if not user_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Check if psychologist_id exists
    psy_exists = False
    for psy_itr in psy_data['psychologist']: 
        if psy_itr['psychologist_id'] == app_dict['psychologist_id']:
            psy_exists = True
    if not psy_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Psychologist not found")

    # Check if the day is within the psychologist's availability
    psy_found = False
    psy : Psychologist
    for psy_itr in psy_data['psychologist']: 
        if psy_itr['psychologist_id'] == app_dict['psychologist_id']:
            psy_found = True
            psy = psy_itr
    if not psy_found: 
        return "Psychologist is not found!"  
    psychologist_availability = psy['availability']
    if app_dict['day'] not in psychologist_availability:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid day for the psychologist's availability")
    
    # Empty list handling
    if not app_data['appointment']:
        app_data['appointment'].append(app_dict)
        write_data(app_data)
        return "Successfully added appointment!"

    # Continue with the appointment creation logic
    for app_itr in app_data['appointment']: 
        if app_itr['appointment_id'] == app.appointment_id:
            return "Appointment ID has to be unique!"
        else:
            app_data['appointment'].append(app_dict)
            write_data(app_data)
            return "Successfully added appointment!"

@router.put('/')
async def update_app(app : Appointment, cur_user: User = Depends(get_current_active_admin_user)):
	app_dict = dict(app)
	app_found = False 
	
    #Asumsi bisa terdapat 2 psikolog dengan nama sama
	for app_idx, app_itr in enumerate(app_data['user']): 
		if app_itr['appointment_id'] == app_dict['appointment_id']: 
			app_found = True
			app_data['appointment'][app_idx] = app_dict
			write_data(app_data)
			return "Successfully updated appointment with ID " + app_dict['appointment_id'] + " and name " + app_dict['name']
	if not app_found: 
		return "Appointment not found!"

@router.delete("/{appointment_id}")
async def delete_app(app_id : int, cur_user: User = Depends(get_current_active_admin_user)): 
	app_found = False
	for app_idx, app_itr in enumerate(app_data['appointment']): 
		if app_itr['appointment_id'] == app_id:
			app_found = True
			app_data['appointment'].pop(app_idx)
			write_data(app_data)
			return "Successfully deleted appointment!"
	if not app_found: 
		return "Appointment not found!"