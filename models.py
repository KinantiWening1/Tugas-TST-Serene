from typing import Union, List
from pydantic import BaseModel

#User
class User(BaseModel):
	user_id: int
	username: str
	email: str
	password: str
	hashed_password: str
	date_of_birth: str
	gender: str
	day: List[int]  
	preference: str  
	disabled: bool
	tags: str

#Psychologist 
class Psychologist(BaseModel):
    psychologist_id: int
    name: str
    qualifications: str
    specialty: str
    availability: List[int]

#Authentication
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class UserInDB(User):
    hashed_password: str