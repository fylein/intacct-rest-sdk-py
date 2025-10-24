import os

from intacctsdk.constants import BASE_URL
from intacctsdk.enums import RESTMethodEnum
from intacctsdk.apis import (
    Bills,
    ApiBase,
    Accounts,
    Entities,
    Dimensions
)


class IntacctRESTSDK:
    """
    Intacct REST SDK
    """
    def __init__(
        self,
        refresh_token: str,
        client_id: str = None,
        client_secret: str = None,
        entity_id: str = None
    ) -> None:
        """
        Initialize connection to Intacct
        :param refresh_token: Intacct refresh_token
        :param client_id: Intacct client_id
        :param client_secret: Intacct client_secret
        :param entity_id: Intacct entity_id
        :return: None
        """
        self.__entity_id = entity_id
        self.__refresh_token = refresh_token
        self.__client_id = os.getenv('INTACCT_CLIENT_ID') or client_id
        self.__client_secret = os.getenv('INTACCT_CLIENT_SECRET') or client_secret

        self._api_instances = []

        self.bills = Bills(self)
        self.accounts = Accounts(self)
        self.entities = Entities(self)
        self.dimensions = Dimensions(self)
        self.api_base = ApiBase(self, object_path='/oauth2/token')

        self.__update_entity_id()
        self.__generate_access_token()
        self.__update_access_token()

    def __generate_access_token(self):
        """
        Generate the access token using the refresh token.
        """
        payload = {
            'grant_type': 'refresh_token',
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'refresh_token': self.__refresh_token
        }

        response = self.api_base._make_request(
            url=f'{BASE_URL}/oauth2/token',
            method=RESTMethodEnum.POST,
            data=payload,
            use_api_headers=False
        )

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

    def _register_api_instance(self, api_instance: ApiBase) -> None:
        """
        Register an API instance for bulk configuration updates.
        :param api_instance: API instance to register
        :return: None
        """
        self._api_instances.append(api_instance)

    @property
    def refresh_token(self) -> str:
        """
        Get the refresh token
        :return: refresh token
        """
        return self.__refresh_token
