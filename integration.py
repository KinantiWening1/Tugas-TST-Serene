import requests
from fastapi import HTTPException

url = 'https://movie-rec-18221162.azurewebsites.net/'

def get_movie_recommendation(mood: str, amount: int):
    login_response = requests.post(url + 'users/login', json={'username': 'asih', 'password': 'pw'})

    # Check if the login was successful
    if login_response.status_code == 200:
        access_token = login_response.json().get('access_token')
        headers = {'Authorization': f'Bearer {access_token}'}

        # Include mood and amount as query parameters
        params = {'mood': mood, 'max_amount': amount}

        # Use params parameter for including query parameters
        movies = requests.post(url + 'movies/recommendations/', headers=headers, params=params)

        return movies.json()
    else:
        raise HTTPException(status_code=login_response.status_code, detail="Login failed")
    
def get_all_movies():
    login_response = requests.post(url + 'users/login', json={'username': 'asih', 'password': 'pw'})

    # Check if the login was successful
    if login_response.status_code == 200:
        access_token = login_response.json().get('access_token')
        headers = {'Authorization': f'Bearer {access_token}'}

        # Use params parameter for including query parameters
        movies = requests.get(url + 'movies', headers=headers)

        return movies.json()
    else:
        raise HTTPException(status_code=login_response.status_code, detail="Login failed")
