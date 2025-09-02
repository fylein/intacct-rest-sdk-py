"""
Intacct Entities API
"""

from .api_base import ApiBase


class Entities(ApiBase):
    """
    Intacct Entities API
    """

    def __init__(self, sdk_instance=None):
        super().__init__(sdk_instance, object_path='/objects/company-config/entity')
