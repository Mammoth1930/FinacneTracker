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

"""
def parse_transactions_json(res:dict) -> pd.DataFrame:
    # A 2D list containing the information for each individual transaction
    transactions = []

    # Extract the data for each transaction as a list and append it to the transactions list
    for transaction in res['data']:
        is_categorizable = transaction['attributes']['isCategorizable']
        been_held = transaction['attributes']['holdInfo'] is not None
        round_up = transaction['attributes']['roundUp'] is not None
        cash_back = transaction['attributes']['cashback'] is not None
        foreign = transaction['attributes']['foreignAmount'] is not None
        card_purchase = transaction['attributes']['cardPurchaseMethod'] is not None
        transfer_account = transaction['relationships']['transferAccount']['data'] is not None
        has_category = transaction['relationships']['category']['data'] is not None

        transactions.append([
            transaction['id'],
            transaction['attributes']['status'],
            transaction['attributes']['rawText'],
            transaction['attributes']['description'],
            transaction['attributes']['message'],
            1 if is_categorizable else 0,
            1 if been_held else 0,
            transaction['attributes']['holdInfo']['amount']['valueInBaseUnits'] if been_held else 0,
            transaction['attributes']['roundUp']['amount']['valueInBaseUnits'] if round_up else 0,
            transaction['attributes']['roundUp']['boostPortion']['valueInBaseUnits'] if round_up else 0,
            transaction['attributes']['cashback']['description'] if cash_back else None,
            transaction['attributes']['cashback']['amount']['valueInBaseUnits'] if cash_back else 0,
            transaction['attributes']['amount'],
            transaction['attributes']['foreignAmount']['currencyCode'] if foreign else None,
            transaction['attributes']['foreignAmount']['valueInBaseUnits'] if foreign else 0,
            transaction['attributes']['cardPurchaseMethod']['method'] if card_purchase else None,
            transaction['attributes']['cardPurchaseMethod']['cardNumberSuffix'] if card_purchase else None,
            transaction['attributes']['settledAt'],
            transaction['attributes']['createdAt'],
            transaction['relationships']['account']['data']['id'],
            transaction['relationships']['transferAccount']['data']['id'] if transfer_account else None,
            transaction['relationships']['category']['data']['id'] if has_category else None,
            transaction['relationships']['parentCategory']['data']['id'] if has_category else None
        ])
    
    return pd.DataFrame(transactions, columns=[
        'id',
        'status',
        'rawText',
        'description',
        'message',
        'isCategorizable',
        'held',
        'heldAmount',
        'roundUpAmount',
        'boostProportion',
        'cashbackDesc',
        'cashbackAmount',
        'amount',
        'foreignCurrency',
        'foreignAmount',
        'cardPurchaseMethod',
        'cardNumberSuffix',
        'settledAt',
        'createdAt',
        'account',
        'transferAccount',
        'category',
        'parentCategory'

    ])

"""

"""
def parse_transaction_json(res:dict) -> pd.DataFrame:
    # A 2D list containing the information for each individual transaction
    transactions = []

    # Extract the data for each transaction as a list and append it to the transactions list
    for transaction in res['data']:
        is_categorizable = transaction['attributes']['isCategorizable']
        been_held = transaction['attributes']['holdInfo'] is not None
        round_up = transaction['attributes']['roundUp'] is not None
        cash_back = transaction['attributes']['cashback'] is not None
        foreign = transaction['attributes']['foreignAmount'] is not None
        card_purchase = transaction['attributes']['cardPurchaseMethod'] is not None
        transfer_account = transaction['relationships']['transferAccount']['data'] is not None
        has_category = transaction['relationships']['category']['data'] is not None

        transactions.append([
            transaction['id'],
            transaction['attributes']['status'],
            transaction['attributes']['rawText'],
            transaction['attributes']['description'],
            transaction['attributes']['message'],
            1 if is_categorizable else 0,
            1 if been_held else 0,
            transaction['attributes']['holdInfo']['amount']['valueInBaseUnits'] if been_held else 0,
            transaction['attributes']['roundUp']['amount']['valueInBaseUnits'] if round_up else 0,
            transaction['attributes']['roundUp']['boostPortion']['valueInBaseUnits'] if round_up else 0,
            transaction['attributes']['cashback']['description'] if cash_back else None,
            transaction['attributes']['cashback']['amount']['valueInBaseUnits'] if cash_back else 0,
            transaction['attributes']['amount'],
            transaction['attributes']['foreignAmount']['currencyCode'] if foreign else None,
            transaction['attributes']['foreignAmount']['valueInBaseUnits'] if foreign else 0,
            transaction['attributes']['cardPurchaseMethod']['method'] if card_purchase else None,
            transaction['attributes']['cardPurchaseMethod']['cardNumberSuffix'] if card_purchase else None,
            transaction['attributes']['settledAt'],
            transaction['attributes']['createdAt'],
            transaction['relationships']['account']['data']['id'],
            transaction['relationships']['transferAccount']['data']['id'] if transfer_account else None,
            transaction['relationships']['category']['data']['id'] if has_category else None,
            transaction['relationships']['parentCategory']['data']['id'] if has_category else None
        ])
    
    return pd.DataFrame(transactions, columns=[
        'id',
        'status',
        'rawText',
        'description',
        'message',
        'isCategorizable',
        'held',
        'heldAmount',
        'roundUpAmount',
        'boostProportion',
        'cashbackDesc',
        'cashbackAmount',
        'amount',
        'foreignCurrency',
        'foreignAmount',
        'cardPurchaseMethod',
        'cardNumberSuffix',
        'settledAt',
        'createdAt',
        'account',
        'transferAccount',
        'category',
        'parentCategory'

    ])

"""

"""
def parse_tags_json(res:dict) -> pd.DataFrame:
    pass

"""
Makes a GET request to the Up Banking API, parses the response, and returns a
DataFrame with the same schema as the corresponding database table.

Params:
    endpoint: The API endpoint that is being queried. Note that this should
        only be the endpoint and not the entire URL and should NOT contain a
        leading "/".

    payload: A dictionary of parameters for the API request.

Requires:
    endpoint: The endpoint must be one of 'accounts', 'transactions', 
        'transactions/{id}', 'tags' otherwise None will be returned.

Returns:
    pd.DataFrame: A Pandas DataFrame containing the information provided by the
        API response. This DataFrame will have the same schema as the database
        table where all the information provided by this endpoint is stored.

    None: None is returned if any of the API requests returns a status code !=
        200 or if the provided endpoint is not one of the required values.
"""
def get_from_api(endpoint: str, payload: dict={}) -> pd.DataFrame:
    url = BASE_URI+endpoint
    final_table = None
    
    while (url != None):
        # Make a GET request to the API using the URL
        response = requests.get(url, headers=AUTH_HEADER, params=payload)

        # API returned an error status code
        if response.status_code != 200:
            print(
                f"There was an error when attempting to get the {endpoint[:-1]} information.\n" +
                f"URL: {response.request.url}\n" +
                f"Status: {response.status_code}\n"
                f"Error: {response.args[0]}"
            )
            return None
        
        # Parse response
        if endpoint == 'accounts':
            final_table = parse_accounts_json(response.json())

        elif endpoint == 'transactions' and '/' in endpoint:
            final_table = parse_transaction_json(response.json())

        elif endpoint == 'transactions':
            final_table = parse_transactions_json(response.json())

        elif endpoint == 'tags':
            final_table = parse_tags_json(response.json())

        else:
            # Provided endpoint isn't what is expected
            print(f"ERROR! {endpoint} is not one of the expected endpoints.")
            return None
        
        # Get the continuation url if it exists
        url = response.json()['links']['next']

    return final_table


"""
Updates the database to contain all of the most recent information available via
the API.
"""
def update_dataset():
    # Update account information
    accounts = get_from_api('accounts')
    if accounts is not None:
        upsert_accounts(accounts)

    # Update transaction information
    # Get all transactions that have happened since last sync
    latest_trans_date = execute_query("SELECT MAX(createdAt) FROM Transactions")
    transactions = get_from_api(
        'transactions',
        {'filter[since]': latest_trans_date.iloc[0][0]}
    )

    if transactions is not None:
        upsert_transactions(transactions)

    # Get all transactions that may have changed/updated
    held_trans = execute_query(
        '''
        SELECT id 
        FROM Transactions 
        WHERE Status != "SETTLED"
            OR category IS NULL
        '''
    )

    for i, row in held_trans.iterrows():
        transactions = get_from_api(f"transactions/{row['id']}")

        if transactions is not None:
            upsert_transactions()

    # Update tag information


# Get access token
access_token = get_secret('Up', 'PAT')

headers = {'Authorization': f'Bearer {access_token}'}

response = requests.get('https://api.up.com.au/api/v1/util/ping', headers=headers)

print(response.json())