from typing import Dict, List, Optional

from intacctsdk.apis.api_base import ApiBase
from intacctsdk.constants import BASE_URL, PAGE_SIZE
from intacctsdk.enums import RESTMethodEnum


class ReportingPeriods(ApiBase):
    """
    Intacct Reporting Periods API
    """

    def __init__(self, sdk_instance: 'IntacctRESTSDK' = None):
        """
        Initialize the Reporting Periods API
        :param sdk_instance: Intacct REST SDK instance
        :return: None
        """
        super().__init__(sdk_instance, object_path='/objects/general-ledger/reporting-period')
