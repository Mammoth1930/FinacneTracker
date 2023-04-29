import requests
import json
import pandas as pd

from handleSecrets import *
from database import *
from helpers import remove_emojis

# Base URI for the Up banking API
BASE_URI = "https://api.up.com.au/api/v1/"

# PAT for Up banking API
PAT = get_secret('Up', 'PAT')

# Authorization header for Up API
AUTH_HEADER = {'Authorization': f'Bearer {PAT}'}

"""
Parses the JSON response provided by the Up banking Accounts API.

Params:
    res: A dictionary representing the JSON response provided by the API.

Returns:
    pd.DataFrame: A Pandas DataFrame with the same schema as the Accounts
        table from the database. This DataFrame will contain all relevant
        account information from the API response JSON.
"""
def parse_accounts_json(res:dict) -> pd.DataFrame:
    # A 2D list containing the information for each individual account
    accounts = []

    # Extract the data for each account as a list and append it to the accounts list
    for account in res['data']:
        accounts.append([
            account['id'],
            remove_emojis(account['attributes']['displayName']),
            account['attribute']['accountType'],
            account['attribute']['ownershipType'],
            account['balance']['valueInBaseUnits'],
            account['createdAt']
        ])

    return pd.DataFrame(accounts, columns=[
            'id',
            'displayName',
            'accountType',
            'ownershipType', 
            'balance',
            'created'
        ])

"""
Uses the API to get all available account information and returns the result as
a DataFrame with the same schema as the Accounts table from the database.

Returns:
    pd.DataFrame: A Pandas DataFrame containing all account information with 
        the same schema as the Accounts table from the database.

    None: This is returned if any of the API requests return a status code !=
        200.
"""
def get_accounts() -> pd.DataFrame:
    url = BASE_URI+'accounts'
    accounts = None

    while (url != None):
        # Make a request to the API using the URL
        response = requests.get(url, headers=AUTH_HEADER)

        # API returns error status code
        if response.status_code != 200:
            print("There was an error when attempting to get the account information.")
            print(f"Url: {response.request.url}")
            print(f"Status: {response.status_code}")
            return None
        
        # Parse response and return the result
        account = parse_accounts_json(response.json())

        # Add individual account to the master DataFame
        if accounts == None:
            accounts = account
        else:
            accounts = pd.concat([accounts, account], ignore_index=True)

        # Get the continuation url if there is one
        url = response.json()['links']['next']

    return accounts


"""
Updates the database to contain all of the most recent information available via
the API.
"""
def update_dataset():
    # Update account information
    accounts = get_accounts()

    if accounts == None:
        return
    
    upsert_accounts(accounts)

    # Update transaction information

    # Update tag information


# Get access token
access_token = get_secret('Up', 'PAT')

headers = {'Authorization': f'Bearer {access_token}'}

response = requests.get('https://api.up.com.au/api/v1/util/ping', headers=headers)

print(response.json())