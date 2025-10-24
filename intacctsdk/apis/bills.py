from intacctsdk.apis.api_base import ApiBase


class Bills(ApiBase):
    """
    Intacct Bills API
    """
    def __init__(self, sdk_instance: 'IntacctRESTSDK' = None):
        """
        Initialize the Bills API
        :param sdk_instance: Intacct REST SDK instance
        :return: None
        """
        super().__init__(sdk_instance, object_path='/objects/accounts-payable/bill')
