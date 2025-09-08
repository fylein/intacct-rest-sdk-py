"""
Intacct Bills API
"""

from .api_base import ApiBase


class Bills(ApiBase):
    """
    Intacct Bills API
    """

    def __init__(self, sdk_instance=None):
        super().__init__(sdk_instance, object_path='/objects/accounts-payable/bill')
