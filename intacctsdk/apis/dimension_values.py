from intacctsdk.apis.api_base import ApiBase


class DimensionValues(ApiBase):
    """
    Intacct Dimension Values API
    """
    def __init__(self, sdk_instance: 'IntacctRESTSDK' = None):
        """
        Initialize the Dimension Values API
        :param sdk_instance: Intacct REST SDK instance
        :return: None
        """
        super().__init__(sdk_instance)
