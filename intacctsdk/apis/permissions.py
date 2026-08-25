from intacctsdk.apis.api_base import ApiBase


class Permissions(ApiBase):
    """
    Intacct permission definitions API.
    Permission records are read-only. Use their ``key`` when assigning a
    permission to a role.
    """
    def __init__(self, sdk_instance: 'IntacctRESTSDK' = None):
        """
        Initialize the Permissions API.
        :param sdk_instance: An instance of the IntacctRESTSDK class.
        :return: None
        """
        super().__init__(
            sdk_instance,
            object_path='/objects/company-config/permission',
            page_size=500,
        )
