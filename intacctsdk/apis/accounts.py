"""
Intacct Accounts API
"""

from .api_base import ApiBase


class Accounts(ApiBase):
    """
    Intacct Accounts API
    """

    def __init__(self, sdk_instance=None):
        super().__init__(sdk_instance, object_path='/objects/general-ledger/account')
