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

    def get_all_generator(
        self,
        fields: List[str],
        filters: List[Dict] = [],
        filter_expression: Optional[str] = None,
        filter_parameters: Dict = {},
        order_by: List[Dict] = [],
        dimension_name: Optional[str] = None
    ):
        """
        Get all reporting periods using the query service
        :param fields: list of fields to fetch
        :param filters: list of filters to apply
        :param filter_expression: filter expression to apply
        :param filter_parameters: filter parameters to apply
        :param order_by: list of fields to order by
        :param dimension_name: unused for reporting periods
        :return: generator of reporting period batches
        """
        start = 1

        if not filter_expression and filters:
            filter_expression = 'and'

        while True:
            response = self._make_request(
                method=RESTMethodEnum.POST,
                url=f'{BASE_URL}/services/core/query',
                data={
                    'object': 'objects/general-ledger/reporting-period',
                    'fields': fields,
                    'filters': filters,
                    'filterExpression': filter_expression,
                    'filterParameters': filter_parameters,
                    'orderBy': order_by,
                    'start': start,
                    'size': PAGE_SIZE
                }
            )

            yield response['ia::result']

            if response.get('ia::meta', {}).get('next') is None:
                break

            start += PAGE_SIZE
