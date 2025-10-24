import os
import json
import requests
import traceback
from dotenv import load_dotenv

from intacctsdk import IntacctRESTSDK
from intacctsdk.constants import TOKEN_URL
from intacctsdk.exceptions import InvalidTokenError, BadRequestError, InternalServerError

load_dotenv()

REDIRECT_URI = 'https://sage-intacct-oauth-redirect-uri.example.com'  # put your redirect uri here
TOKEN_FILE = 'tokens.json'
INTACCT_CLIENT_ID = os.getenv('INTACCT_CLIENT_ID')
INTACCT_CLIENT_SECRET = os.getenv('INTACCT_CLIENT_SECRET')


def store_refresh_token(refresh_token: str) -> None:
    """
    Store the refresh token in a file
    :param refresh_token: Refresh token
    :return: None
    """
    with open(TOKEN_FILE, 'w') as f:
        json.dump({'refresh_token': refresh_token}, f)


def _make_token_request(data: dict) -> dict:
    """
    Common function to make token requests to Intacct API.
    :param data: Data to send in the request
    :return: Response from the request
    """
    response = requests.post(
        url=TOKEN_URL,
        data=data
    )
    print('Status code:', response.status_code, 'Response:', response.text)
    return response.json()


def exchange_code_and_store_refresh_token(code: str) -> str:
    """
    Exchange the code for a refresh token and store it in a file
    :param code: Code to exchange
    :return: Refresh token
    """
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


def exchange_refresh_token_for_access_token(refresh_token: str) -> str:
    """
    Exchange the refresh token for an access token
    :param refresh_token: Refresh token
    :return: Access token
    """
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': os.getenv('INTACCT_CLIENT_ID'),
        'client_secret': os.getenv('INTACCT_CLIENT_SECRET')
    }

    tokens = _make_token_request(data)
    store_refresh_token(tokens['refresh_token'])

    return tokens['access_token']


def main() -> None:
    """
    Entry Point
    """
    tokens = {}
    try:
        with open(TOKEN_FILE, 'r') as f:
            tokens = json.load(f)
    except FileNotFoundError:
        print(f"Error: {TOKEN_FILE} file not found")

    refresh_token = tokens.get('refresh_token')

    if not refresh_token:
        print("Please open the following URL in your browser and authorize the app, then copy the code from the redirect URL and paste it here")
        print(f"https://api.intacct.com/ia/api/v1/oauth2/authorize?response_type=code&client_id={INTACCT_CLIENT_ID}&redirect_uri={REDIRECT_URI}&state=1&scope=offline_access")

        code = input("Enter the code: ")

        refresh_token = exchange_code_and_store_refresh_token(code)

    try:
        sdk = IntacctRESTSDK(
            refresh_token=refresh_token,
            # entity_id='200' # put your entity id here if you want to use a specific entity
        )
        store_refresh_token(sdk.refresh_token)

        # Get specific fields for accounts with filters, sorting, etc.
        accounts_generator = sdk.accounts.get_all_generator(
            fields=['id', 'name', 'key', 'status'],
            filters=[
                {
                    "$eq": {
                        "status": "inactive"
                    }
                },
                {
                    "$gte": {
                        "audit.modifiedDateTime": "2025-05-01T07:13:58Z"
                    }
                }
            ]
        )
        for account in accounts_generator:
            print(account)

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


if __name__ == '__main__':
    main()
