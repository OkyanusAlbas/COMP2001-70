import requests

AUTH_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def get_auth_users():
    response = requests.get(AUTH_API_URL, timeout=5)
    response.raise_for_status()
    return response.json()
