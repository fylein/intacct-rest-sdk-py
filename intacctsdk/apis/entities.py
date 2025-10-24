from intacctsdk.apis.api_base import ApiBase


class Entities(ApiBase):
    """
    Intacct Entities API
    """
    def __init__(self, sdk_instance: 'IntacctRESTSDK' = None):
        """
        Initialize the Entities API
        :param sdk_instance: Intacct REST SDK instance
        :return: None
        """
        super().__init__(sdk_instance, object_path='/objects/company-config/entity')
