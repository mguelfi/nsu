from .base import NessusEndpoint

class PermissionsAPI(NessusEndpoint):
    def change(self, object_type, object_id, *acls):
        '''
        Modify the permission of a specific object.

        `permissions: change </api#/resources/permissions/change>`_

        Args:
            otype (str):
                The type of object to change.
            id (int):
                The unique identifier fo the object.
            *acls (dict):
                ACL dictionaries inform Tenable.io how to handle permissions of
                the various objects within Tenable.io.  The permissions dict is
                described on the `permissions resource`_ page.  Further the
                integer values that represent the permissions granted are
                detailed on the `authorization page`_ within the documentation.

        Returns:
            None: The object permissions were successfully changed.

        .. _permissions resource:
            /api#/resources/permissions
        .. _authorization page:
            /api#/authorization
        '''
        # Check to make sure all of the ACLs are dictionaries.
        for item in acls:
            self._check('acl', item, dict)

        # Make the API call.
        self._api.put('permissions/{}/{}'.format(
            self._check('object_type', object_type, str),
            self._check('object_id', object_id, int)
        ), json={'acls': acls})

    def list(self, object_type, object_id):
        '''
        List the permissions of a specific object.

        `permissions: list </api#/resources/permissions/list>`_

        Args:
            otype (str):
                The type of object being queried.
            id (int):
                The unique identifier of the object.

        Returns:
            list: 
                The permission recourse record listings for the specified object.
        '''
        return self._api.get(
            'permissions/{}/{}'.format(
                self._check('object_type', object_type, str),
                self._check('object_id', object_id, int)
            )).json()['acls']

