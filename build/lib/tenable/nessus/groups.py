from .base import NessusEndpoint

class GroupsAPI(NessusEndpoint):
    def add_user(self, group_id, user_id):
        '''
        Add a user to a user group.

        `groups: add-user </api#/resources/groups/add-user>`_

        Args:
            group_id (int):
                The unique identifier of the group to add the user to.
            user_id (int):
                The unique identifier of the user to add.

        Examples:
            >>> nessus.groups.add_user(1, 1)
        '''
        self._api.post('groups/{}/users/{}'.format(
            self._check('group_id', group_id, int),
            self._check('user_id', user_id, int), json={}
        ))

    def create(self, name):
        '''
        Create a new user group.

        `groups: create </api#/resources/groups/create>`_

        Args:
            name (str):
                The name of the group that will be created.

        Returns:
            dict: The group resource record of the newly minted group.

        Examples:
            >>> group = nessus.groups.create('Group Name')
        '''
        return self._api.post('groups', json={
            'name': self._check('name', name, str)
        }).json()

    def delete(self, *ids):
        '''
        Delete a user group.

        `groups: delete </api#/resources/groups/delete>`_

        Args:
            id (int): The unique identifier for the group to be deleted.

        Examples:
            >>> nessus.groups.delete(1)
        '''
        if len(ids) <= 1:
            # if only a singular gorup id was passed
            self._api.delete('groups/{}'.format(
                self._check('ids', ids[0], int)))
        else:
            # if multiple group ids were requested to be deleted, then we will
            # call the bulk deletion API.
            return self._api.delete(
                'groups',
                json={'ids': [self._check('ids', i, int) for i in ids]}).json()

    def delete_user(self, group_id, user_id):
        '''
        Delete a user from a user group.

        `groups: delete-user </api#/resources/groups/delete-user>`_

        Args:
            group_id (int): 
                The unique identifier for the group to be modified.
            user_id (int): 
                The unique identifier for the user to be removed from the group.

        Examples:
            >>> nessus.groups.delete_user(1, 1)
        '''
        self._api.delete('groups/{}/users/{}'.format(
            self._check('group_id', group_id, int),
            self._check('user_id', user_id, int)
        ))

    def edit(self, id, name):
        '''
        Edit a user group.

        groups: edit </api#/resources/groups/edit>`_

        Args:
            id (int):
                The unique identifier for the group to be modified.
            name (str):
                The new name for the group.

        Examples:
            >>> nessus.groups.edit(1, 'Updated name')
        '''
        self._api.put('groups/{}'.format(self._check('id', id, int)), 
            json={'name': self._check('name', name, str)})

    def list(self):
        '''
        Lists all of the available user groups.

        groups: list </api#/resources/groups/list>`_

        Returns:
            list: List of the group resource records

        Examples:
            >>> for group in nessus.groups.list():
            ...     pprint(group)
        '''
        return self._api.get('groups').json()['groups']

    def list_users(self, id):
        '''
        List the user memberships within a specific user group.

        `groups: list-users </api#/resources/groups/list-users>`_

        Args:
            id (int): The unique identifier of the group requested.

        Returns:
            list: 
                List of user resource records based on membership to the
                specified group.

        Example:
            >>> for user in nessus.groups.list_users(1):
            ...     pprint(user)
        '''
        return self._api.get('groups/{}/users'.format(
            self._check('id', id, int))).json()['users']

