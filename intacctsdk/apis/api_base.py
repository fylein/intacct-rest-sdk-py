"""
API Base class with util functions
"""
import json
from typing import List, Dict

import requests

from intacctsdk.constants import BASE_URL
from intacctsdk.exceptions import IntacctRESTSDKError, BadRequestError, InternalServerError


class ApiBase:
    """The base class for all API classes."""

    def __init__(self, sdk_instance=None, object_path:str=None):
        self.__access_token = None
        self.__entity_id = None
        self.__object_path = object_path
        self.__object_name = object_path.replace('/objects/', '')
        self._sdk_instance = sdk_instance

        if sdk_instance:
            sdk_instance._register_api_instance(self)

    def update_access_token(self, access_token):
        """
        Sets the access token for APIs
        :param access_token: acceess token (JWT)
        :return: None
        """
        self.__access_token = access_token

    def update_entity_id(self, entity_id):
        """
        Sets the entity id for APIs
        :param entity_id: entity id
        :return: None
        """
        self.__entity_id = entity_id

    def _make_request(self, url: str, method: str, data: dict = {}, params: dict = {}, use_api_headers: bool = True) -> List[Dict] or Dict:
        """
        Makes a request to the API
        :param method: HTTP method
        :param data: data to send
        :return: response
        """
        api_headers = {
            'Authorization': 'Bearer {0}'.format(self.__access_token),
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-IA-API-Param-Entity': self.__entity_id if self.__object_path != '/objects/company-config/entity' else None
        }
        print('Method', method, 'URL', url, 'Data', json.dumps(data), 'Use API Headers', use_api_headers, 'Headers', api_headers)
        response = requests.request(method=method, url=url, data=json.dumps(data) if use_api_headers and method != 'GET' else data, params=params, headers=api_headers if use_api_headers else {})

        if response.status_code >= 200 and response.status_code < 300:
            return response.json()

        elif response.status_code >= 400 and response.status_code < 500:
            raise BadRequestError('Something wrong with the request body', response.text)

        elif response.status_code >= 500:
            raise InternalServerError('Internal server error', response.text)

        else:
            raise IntacctRESTSDKError('Error: {0}'.format(response.status_code), response.text)


    def _get_request(self, params: dict = None) -> List[Dict] or Dict:
        """Create a HTTP GET request.

        Parameters:
            api_url (str): Url for the wanted API.

        Returns:
            A response from the request (dict).
        """
        url = f'{BASE_URL}{self.__object_path}'

        return self._make_request(method='GET', url=url, params=params)


    def get_all_generator(self, fields: List[str], filters: List[Dict] = [], filter_expression: str = None, filter_parameters: Dict = {}, order_by: List[Dict] = [], dimension_name: str = None) -> List[Dict]:
        """
        Get all objects from the API using user query service
        :param fields: list of fields to fetch
        :return: generator of objects
        """
        start = 1
        page_size = 2000

        if not filter_expression and filters:
            filter_expression = 'and'

        while True:
            response = self._make_request(
                method='POST',
                url=f'{BASE_URL}/services/core/query',
                data={
                    'object': f'platform-apps/nsp::{dimension_name.lower()}' if dimension_name else self.__object_name,
                    'fields': fields,
                    'filters': filters,
                    'filterExpression': filter_expression,
                    'filterParameters': filter_parameters,
                    'orderBy': order_by,
                    'start': start,
                    'size': page_size
                }
            )

            yield response['ia::result']

            if response.get('ia::meta', {}).get('next') is None:
                break

            start += page_size

    def count(self, filters: List[Dict] = [], filter_expression: str = None, filter_parameters: Dict = {}, dimension_name: str = None):
        if not filter_expression and filters:
            filter_expression = 'and'
        
        response = self._make_request(method='POST', url=f'{BASE_URL}/services/core/query', data={
            'object': f'platform-apps/nsp::{dimension_name.lower()}' if dimension_name else self.__object_name,
            'filters': filters,
            'filterExpression': filter_expression,
            'filterParameters': filter_parameters,
            'start': 1,
            'size': 1
        })

        return response['ia::meta']['totalCount']

    def get_by_id(self, id: str) -> Dict:
        """Get an object by id"""
        return self._make_request(method='GET', url=f'{BASE_URL}{self.__object_path}/{id}')

    def get_model(self) -> Dict:
        """Get the model for the object"""
        return self._make_request(method='GET', url=f'{BASE_URL}/services/core/model', params={
            'name': self.__object_name
        })
