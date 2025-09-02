"""
Intacct Dimensions API
"""

from typing import List, Dict

from .api_base import ApiBase


class Dimensions(ApiBase):
    """
    Intacct Dimensions API
    """

    def __init__(self, sdk_instance=None):
        super().__init__(sdk_instance, object_path='/services/company-config/dimensions/list')

    def list(self):
        return self._get_request().get('ia::result')
