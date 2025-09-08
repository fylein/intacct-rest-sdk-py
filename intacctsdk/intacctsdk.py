"""
Intacct REST SDK
"""
import os
from intacctsdk.apis import *
from .constants import BASE_URL


class IntacctRESTSDK:
    """
    Intacct REST SDK
    """

    def __init__(self, refresh_token: str, client_id: str = None, client_secret: str = None, entity_id: str = None):
        """
        Initialize connection to Intacct
        :param client_id: Intacct client_Id
        :param client_secret: Intacct client_secret
        :param refresh_token: Intacct refresh_token
        """
        self.__client_id = os.getenv('INTACCT_CLIENT_ID') or client_id
        self.__client_secret = os.getenv('INTACCT_CLIENT_SECRET') or client_secret
        self.__refresh_token = refresh_token
        self.__entity_id = entity_id

        self._api_instances = []

        self.api_base = ApiBase(self, object_path='/oauth2/token')
        self.accounts = Accounts(self)
        self.entities = Entities(self)
        self.dimensions = Dimensions(self)
        self.bills = Bills(self)

        self.__generate_access_token()
        self.__update_access_token()
        self.__update_entity_id()

    def __generate_access_token(self):
        """Get the access token using a HTTP post.

        Returns:
            A new access token.
        """
        api_data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.__refresh_token,
            'client_id': self.__client_id,
            'client_secret': self.__client_secret
        }
        response = self.api_base._make_request(url=f'{BASE_URL}/oauth2/token', method='POST', data=api_data, use_api_headers=False)

        self.__access_token = response['access_token']
        self.__refresh_token = response['refresh_token']

    def __update_access_token(self):
        """
        Update the access token and change it in all registered API objects.
        """
        for api_instance in self._api_instances:
            api_instance.update_access_token(self.__access_token)

    def __update_entity_id(self):
        """
        Update the entity id and change it in all registered API objects.
        """
        for api_instance in self._api_instances:
            api_instance.update_entity_id(self.__entity_id)

    def _register_api_instance(self, api_instance):
        """
        Register an API instance for bulk configuration updates.
        """
        self._api_instances.append(api_instance)

    @property
    def refresh_token(self):
        """
        Get the refresh token
        """
        return self.__refresh_token
