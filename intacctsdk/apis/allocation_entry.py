from intacctsdk.apis.api_base import ApiBase


class AllocationEntry(ApiBase):
    """
    Intacct Allocation Entry API
    """
    def __init__(self, sdk_instance: 'IntacctRESTSDK' = None):
        """
        Initialize the Allocation Entry API
        :param sdk_instance: Intacct REST SDK instance
        :return: None
        """
        super().__init__(sdk_instance, object_path='/objects/general-ledger/txn-allocation-template-line')
