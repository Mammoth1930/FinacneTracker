import requests
import pandas as pd

from handleSecrets import *
from database import *
from helpers import remove_emojis, add_second

# Base URI for the Up banking API
BASE_URI = "https://api.up.com.au/api/v1/"

# PAT for Up banking API
PAT = get_secret('Up', 'PAT')

# Authorization header for Up API
AUTH_HEADER = {'Authorization': f'Bearer {PAT}'}

def parse_accounts_json(res: dict) -> pd.DataFrame:
    """
    Parses the JSON response provided by the Up banking Accounts API.

    Params:
        res: A dictionary representing the JSON response provided by the API.

    Returns:
        pd.DataFrame: A Pandas DataFrame with the same schema as the Accounts
            table from the database. This DataFrame will contain all relevant
            account information from the API response JSON.
    """

    # A 2D list containing the information for each individual account
    accounts = []

    # Extract the data for each account as a list and append it to the accounts list
    for account in res['data']:
        accounts.append([
            account['id'],
            remove_emojis(account['attributes']['displayName']),
            account['attributes']['accountType'],
            account['attributes']['ownershipType'],
            account['attributes']['balance']['valueInBaseUnits'],
            account['attributes']['createdAt']
        ])

    return pd.DataFrame(accounts, columns=[
            'id',
            'displayName',
            'accountType',
            'ownershipType', 
            'balance',
            'created'
        ])

def parse_transactions_json(res: dict) -> pd.DataFrame:
    """
    Parses a JSON containing information about several transactions.

    Params:
        res: The JSON response containing the transactional information.

    Require:
        res: Must be in the expected multi transaction format as described in the
            Up banking API documentation.

    Returns:
        DataFrame: A pandas DataFrame with the same schema as the Transactions table
            from the database. This DataFrame contains all of the information
            extracted from the JSON response.
    """

    # A 2D list containing the information for each individual transaction
    transactions = []

    # Extract the data for each transaction as a list and append it to the transactions list
    for transaction in res['data']:
        is_categorizable = transaction['attributes']['isCategorizable']
        been_held = transaction['attributes']['holdInfo'] is not None
        round_up = transaction['attributes']['roundUp'] is not None
        boost_portion = round_up and transaction['attributes']['roundUp']['boostPortion'] is not None
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
            transaction['attributes']['holdInfo']['amount']['valueInBaseUnits'] if been_held else None,
            transaction['attributes']['roundUp']['amount']['valueInBaseUnits'] if round_up else None,
            transaction['attributes']['roundUp']['boostPortion']['valueInBaseUnits'] if boost_portion else None,
            transaction['attributes']['cashback']['description'] if cash_back else None,
            transaction['attributes']['cashback']['amount']['valueInBaseUnits'] if cash_back else None,
            transaction['attributes']['amount']['valueInBaseUnits'],
            transaction['attributes']['foreignAmount']['currencyCode'] if foreign else None,
            transaction['attributes']['foreignAmount']['valueInBaseUnits'] if foreign else None,
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

def parse_transaction_json(res: dict) -> pd.DataFrame:
    """
    Parses a JSON containing information about a single transactions.

    Params:
        res: The JSON response containing information regarding the transaction.

    Require:
        res: Must be in the expected single transaction format as described in the
            Up banking API documentation.

    Returns:
        DataFrame: A pandas DataFrame with the same schema as the Transactions table
            from the database. This DataFrame contains all of the information
            extracted from the JSON response.
    """

    # A 2D list containing all the information about this transaction
    data = []

    # Extract the data for this transaction
    transaction = res['data']

    # For nullable fields in the JSON response may not show up so these booleans
    # check whether the field is NULL to avoid indexing errors in the mapping
    is_categorizable = transaction['attributes']['isCategorizable']
    been_held = transaction['attributes']['holdInfo'] is not None
    round_up = transaction['attributes']['roundUp'] is not None
    boost_portion = round_up and transaction['attributes']['roundUp']['boostPortion'] is not None
    cash_back = transaction['attributes']['cashback'] is not None
    foreign = transaction['attributes']['foreignAmount'] is not None
    card_purchase = transaction['attributes']['cardPurchaseMethod'] is not None
    transfer_account = transaction['relationships']['transferAccount']['data'] is not None
    has_category = transaction['relationships']['category']['data'] is not None

    data.append([
        transaction['id'],
        transaction['attributes']['status'],
        transaction['attributes']['rawText'],
        transaction['attributes']['description'],
        transaction['attributes']['message'],
        1 if is_categorizable else 0,
        1 if been_held else 0,
        transaction['attributes']['holdInfo']['amount']['valueInBaseUnits'] if been_held else None,
        transaction['attributes']['roundUp']['amount']['valueInBaseUnits'] if round_up else None,
        transaction['attributes']['roundUp']['boostPortion']['valueInBaseUnits'] if boost_portion else None,
        transaction['attributes']['cashback']['description'] if cash_back else None,
        transaction['attributes']['cashback']['amount']['valueInBaseUnits'] if cash_back else None,
        transaction['attributes']['amount']['valueInBaseUnits'],
        transaction['attributes']['foreignAmount']['currencyCode'] if foreign else None,
        transaction['attributes']['foreignAmount']['valueInBaseUnits'] if foreign else None,
        transaction['attributes']['cardPurchaseMethod']['method'] if card_purchase else None,
        transaction['attributes']['cardPurchaseMethod']['cardNumberSuffix'] if card_purchase else None,
        transaction['attributes']['settledAt'],
        transaction['attributes']['createdAt'],
        transaction['relationships']['account']['data']['id'],
        transaction['relationships']['transferAccount']['data']['id'] if transfer_account else None,
        transaction['relationships']['category']['data']['id'] if has_category else None,
        transaction['relationships']['parentCategory']['data']['id'] if has_category else None
    ])
    
    return pd.DataFrame(data, columns=[
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

def parse_tags_json(res: dict) -> pd.DataFrame:
    """

    """

    return pd.DataFrame() # ToDo: this method

def get_from_api(endpoint: str, payload: dict[str, str]={}) -> pd.DataFrame | None:
    """
    Makes a GET request to the Up Banking API, parses the response, and returns a
    DataFrame with the same schema as the corresponding database table.

    Params:
        endpoint: The API endpoint that is being queried. Note that this should
            only be the endpoint and not the entire URL and should NOT contain a
            leading "/".

        payload: A dictionary of parameters for the API request.

    Require:
        endpoint: The endpoint must be one of 'accounts', 'transactions', 
            'transactions/{id}', 'tags' otherwise None will be returned.

    Returns:
        pd.DataFrame: A Pandas DataFrame containing the information provided by the
            API response. This DataFrame will have the same schema as the database
            table where all the information provided by this endpoint is stored.

        None: None is returned if any of the API requests returns a status code !=
            200 or if the provided endpoint is not one of the required values.
    """

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
                f"Error: {response.reason}"
            )
            return None
        
        # Parse response
        if endpoint == 'accounts':
            parsed_response = parse_accounts_json(response.json())

        elif endpoint == 'transactions' and '/' in endpoint:
            parsed_response = parse_transaction_json(response.json())

        elif endpoint == 'transactions':
            parsed_response = parse_transactions_json(response.json())

        elif endpoint == 'tags':
            parsed_response = parse_tags_json(response.json())

        else:
            # Provided endpoint isn't what is expected
            print(f"ERROR! {endpoint} is not one of the expected endpoints.")
            return None
        
        if final_table is None:
            final_table = parsed_response

        else:
            final_table = pd.concat([final_table, parsed_response], ignore_index=True)
        
        # Get the continuation url if it exists
        url = response.json()['links']['next']

    return final_table


def update_dataset() -> None:
    """
    Updates the database to contain all of the most recent information available via
    the API.
    """

    # Update account information
    accounts = get_from_api('accounts')
    if accounts is not None:
        upsert_accounts(accounts)

    # Update transaction information
    # Check to see when the database was last synced and add 1 sec because API filter is inclusive
    latest_trans_date = add_second(read_database("SELECT MAX(createdAt) FROM Transactions").iloc[0][0])
    
    if latest_trans_date is None: # If the database is empty
        latest_trans_date = "1900-01-01T00:00:00+10:00"

    transactions = get_from_api(
        'transactions',
        {'filter[since]': latest_trans_date}
    )

    if transactions is not None:
        upsert_transactions(transactions, True)

    # Get all transactions that may have changed/updated
    change_ids = read_database(
        f'''
        SELECT id 
        FROM Transactions 
        WHERE (Status != "SETTLED" OR category IS NULL)
            AND createdAt < "{latest_trans_date}"
        '''
    )

    for i, row in change_ids.iterrows():
        change_trans = get_from_api(f"transactions/{row['id']}")

        if change_trans is not None:
            upsert_transactions(change_trans, False)

    # ToDo: Update tag information

def tables_to_csv() -> None:
    """
    Writes all the tables in the database to separate .csv files, this is primarily
    intended for debugging purposes.
    """

    # Accounts
    accounts_df = read_database('SELECT * FROM Accounts')
    accounts_df.to_csv('./data/accounts.csv', index=False)

    # Transactions
    transactions_df = read_database('SELECT * FROM Transactions')
    transactions_df.to_csv('./data/transactions.csv', index=False)

    # ToDo: Tags


# Get access token
# access_token = get_secret('Up', 'PAT')

# headers = {'Authorization': f'Bearer {access_token}'}

# response = requests.get('https://api.up.com.au/api/v1/util/ping', headers=headers)

# print(response.json())