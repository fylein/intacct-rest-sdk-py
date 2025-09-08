import os
import json
import traceback

import requests
from dotenv import load_dotenv

from intacctsdk.exceptions import InvalidTokenError, BadRequestError, InternalServerError
from intacctsdk.constants import TOKEN_URL
from intacctsdk import IntacctRESTSDK

load_dotenv()


REDIRECT_URI = 'https://looooloooooooo.com' # put your redirect uri here


def store_refresh_token(refresh_token):
    with open('tokens.json', 'w') as f:
        json.dump({'refresh_token': refresh_token}, f)

def _make_token_request(data):
    """Common function to make token requests to Intacct API."""
    response = requests.post(TOKEN_URL, data=data)
    print('Status code:', response.status_code, 'Response:', response.text)
    return response.json()


def exchange_code_and_store_refresh_token(code):
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': os.getenv('INTACCT_CLIENT_ID'),
        'client_secret': os.getenv('INTACCT_CLIENT_SECRET')
    }

    tokens = _make_token_request(data)
    refresh_token = tokens['refresh_token']

    store_refresh_token(refresh_token)

    return refresh_token


def exchange_refresh_token_for_access_token(refresh_token):
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': os.getenv('INTACCT_CLIENT_ID'),
        'client_secret': os.getenv('INTACCT_CLIENT_SECRET')
    }

    tokens = _make_token_request(data)

    store_refresh_token(tokens['refresh_token'])

    return tokens['access_token']


try:
    with open('tokens.json', 'r') as f:
        tokens = json.load(f)
except FileNotFoundError:
    print("Error: tokens.json file not found")
    tokens = {}

refresh_token = tokens.get('refresh_token')

if not refresh_token:
    print("Please open the following URL in your browser and authorize the app, then copy the code from the redirect URL and paste it here")
    print(f"https://api.intacct.com/ia/api/v1/oauth2/authorize?response_type=code&client_id=b520e1bd6782ec7faeb2.app.sage.com&redirect_uri=https://looooloooooooo.com&state=1&scope=offline_access")
    code = input("Enter the code: ")

    refresh_token = exchange_code_and_store_refresh_token(code)




try:
    sdk = IntacctRESTSDK(
        refresh_token=refresh_token,
        # entity_id='200' # put your entity id here if you want to use a specific entity
    )
    store_refresh_token(sdk.refresh_token)

    # Get specific fields for accounts with filters, sorting, etc.
    # accounts_generator = sdk.accounts.get_all_generator(fields=['id', 'name', 'key', 'status'], filters=[
        # {
        #     "$eq": {
        #         "status": "inactive"
        #     }
        # },
        # {
        #     "$gte": {
        #         "audit.modifiedDateTime": "2025-08-19T07:13:58Z"
        #     }
        # }
    # ])
    # for account in accounts_generator:
    #     print(account)

    # Get a specific account by id
    # account = sdk.accounts.get_by_id('350')
    # print(account)


    # Get all entities
    # entities_generator = sdk.entities.get_all_generator(fields=['id', 'name'])
    # for entity in entities_generator:
    #     print(entity)

    # Get the model for the accounts object
    # model = sdk.accounts.get_model()
    # print(model)

    # Get all dimensions
    # dimensions = sdk.dimensions.list()
    # print(dimensions)


    # Get dimension fields for a specific dimension name
    # dimensions_generator = sdk.dimensions.get_all_generator(dimension_name='NEW_TEAM', fields=['id', 'name'])
    # for dimension in dimensions_generator:
    #     print(dimension)

    # Get the count of accounts with filters
    # count = sdk.accounts.count(filters=[
    #     {
    #         "$eq": {
    #             "status": "inactive"
    #         }
    #     },
    #     {
    #         "$gte": {
    #             "audit.modifiedDateTime": "2025-08-19T07:13:58Z"
    #         }
    #     }
    # ])
    # print(count)

    # Get the count of dimensions for a specific dimension name
    # count = sdk.dimensions.count(dimension_name='NEW_TEAM')
    # print(count)

    # Get all bills with specific fields
    # bills_generator = sdk.bills.get_all_generator(fields=['id'])
    # for bill in bills_generator:
    #     print(bill)

    # Get a specific bill by id
    # bill = sdk.bills.get_by_id('4375')
    # print(bill)


except (InvalidTokenError, BadRequestError, InternalServerError) as e:
    print(e.message, e.response)

except Exception:
    print(traceback.format_exc())
