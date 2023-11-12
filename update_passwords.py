from passlib.context import CryptContext
from auth import get_password_hash  # Make sure to import the correct function
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_filename = "json_data/user.json"

# Load user data from the JSON file
with open(user_filename, "r") as read_file:
    user_data = json.load(read_file)
    print(user_data)

# Assuming you have a function to retrieve user data from the JSON file
def update_password_hash(user_data, new_password):
    user_data["hashed_password"] = get_password_hash(new_password)

# Load user data from the JSON file
with open(user_filename, "r") as file:
    users = json.load(file)["user"]

# Update each user's password hash
for user_data in users:
    # Assuming you have a 'password' field in each user_data
    update_password_hash(user_data, user_data["password"])

# Save the updated user data back to the JSON file
with open(user_filename, "w") as file:
    json.dump({"user": users}, file, indent=2)
