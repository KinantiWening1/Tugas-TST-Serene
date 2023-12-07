from fastapi import APIRouter, HTTPException, Depends
import user_crud, psychologist_crud
from typing import Dict,List
from auth import oauth2_scheme, get_current_active_user
from models import User

# Create a router for the appointment matching
router = APIRouter(tags=["pairing"])

# Create a route for matching users with psychologists for an appointment
@router.get('/{user_id}')
async def match_appointment(user_id: int,cur_user: User = Depends(get_current_active_user)):
    user = await user_crud.get_user(user_id)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Find available psychologists
    available_psychologists = await find_available_psychologists(user['day'])
    
    if not available_psychologists:
        return "Sorry, there are no available psychologists at the moment."
    
    # Match the user with an available psychologist
    matched_psychologist = match_user_with_psychologist(user['preference'], available_psychologists)
    
    if matched_psychologist is None:
        return "Sorry, we couldn't find a suitable psychologist at the moment."
    else:
        return {
            "message": "Appointment matched successfully!",
            "user": user,
            "psychologist": matched_psychologist,
        }

# Helper functions for appointment matching
async def get_user_by_id(user_id: int) -> user_crud.User:
    users = await user_crud.get_all_users()
    for user in users:
        if user.user_id == user_id:
            return user
    return None

async def find_available_psychologists(day: int) -> List[psychologist_crud.Psychologist]:
    available_psychologists = []

    # Use await to call the asynchronous function
    psychologists = await psychologist_crud.get_all_psy()

    for psychologist in psychologists:
        if can_schedule_appointment(day, psychologist['availability']):
            available_psychologists.append(psychologist)

    return available_psychologists

def can_schedule_appointment(day: int, psy_avail: List[int]) -> bool:
    return day in psy_avail

def match_user_with_psychologist(preference: str, psychologists: List[psychologist_crud.Psychologist]) -> psychologist_crud.Psychologist:
    for psychologist in psychologists:
        if psychologist['specialty'] == preference:
            return psychologist  
    return None 
