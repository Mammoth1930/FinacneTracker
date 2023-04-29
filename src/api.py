import requests

from handleSecrets import *

# Base URI for the Up banking API
BASE_URI = "https://api.up.com.au/api/v1/"

# PAT for Up banking API
PAT = get_secret('Up', 'PAT')

# Authorization header for Up API
AUTH_HEADER = {'Authorization': f'Bearer {PAT}'}





# Get access token
access_token = get_secret('Up', 'PAT')

headers = {'Authorization': f'Bearer {access_token}'}

response = requests.get('https://api.up.com.au/api/v1/util/ping', headers=headers)

print(response.json())