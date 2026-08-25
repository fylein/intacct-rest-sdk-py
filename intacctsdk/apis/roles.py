from typing import Dict, List

from intacctsdk.apis.api_base import ApiBase


class Roles(ApiBase):
    """
    Intacct roles API.
    """
    def __init__(self, sdk_instance: 'IntacctRESTSDK' = None):
        """
        Initialize the Roles API.
        :param sdk_instance: An instance of the IntacctRESTSDK class.
        :return: None
        """
        super().__init__(sdk_instance, object_path='/objects/company-config/role')

    def update_permission_assignments(
        self,
        role_key: str,
        permission_assignments: List[Dict]
    ) -> Dict:
        """
        Create or update permission assignments for a role.
        Each assignment requires ``permission_key`` and ``access_rights``.
        :param role_key: The key of the role to update.
        :param permission_assignments: A list of permission assignments to create or update.
        :return: The updated role object.
        """
        role_permission_assignments = []

        for assignment in permission_assignments:
            permission_key = assignment.get('permission_key')
            access_rights = assignment.get('access_rights')
            role_permission_assignments.append({
                'permission': {
                    'key': str(permission_key)
                },
                'accessRights': access_rights
            })

        return self.update(
            key=role_key,
            data={'rolePermissionAssignments': role_permission_assignments}
        )
