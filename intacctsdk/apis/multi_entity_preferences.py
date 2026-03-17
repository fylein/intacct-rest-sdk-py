from typing import Dict
from intacctsdk.apis.api_base import ApiBase


class MultiEntityPreferences(ApiBase):
    """
    Intacct Multi-Entity Preferences API
    
    This API provides access to multi-entity preference setup configuration.
    Note: This endpoint does not support the query service, so it uses direct REST calls.
    """
    def __init__(self, sdk_instance: 'IntacctRESTSDK' = None):
        """
        Initialize the Multi-Entity Preferences API
        :param sdk_instance: Intacct REST SDK instance
        :return: None
        """
        super().__init__(sdk_instance, object_path='/objects/company-config/multi-entity-preference/setup')

    def get(self) -> Dict:
        """
        Get the multi-entity preference setup configuration.
        
        :return: multi-entity preference setup data
        """
        response = self._get_request()
        
        if isinstance(response, dict) and 'ia::result' in response:
            return response['ia::result']
        else:
            return response
