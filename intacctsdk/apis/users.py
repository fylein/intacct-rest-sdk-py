from intacctsdk.apis.api_base import ApiBase


class Users(ApiBase):
    """
    Intacct Users API
    """
    def __init__(self, sdk_instance: 'IntacctRESTSDK' = None):
        """
        Initialize the Users API
        :param sdk_instance: Intacct REST SDK instance
        :return: None
        """
        super().__init__(sdk_instance, object_path='/objects/company-config/user')
