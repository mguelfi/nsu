'''
users
=====

The following methods allow for interaction into the Nessus
 `users </api#/resources/users>`_ API endpoints.

Methods available on ``nessus.users``:

.. rst-class:: hide-signature
.. autoclass:: UsersAPI

    .. automethod:: create
    .. automethod:: change_password
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: gen_api_keys
    .. automethod:: list
'''
from .base import NessusEndpoint
from tenable.errors import UnknownError, PasswordComplexityError
from tenable.utils import dict_merge

class UserAPI(NessusEndpoint):
    def list(self, fields=None):
        '''
        Retrieves the list of scan zone definitions.
        
        + `user: list <https://docs.tenable.com/sccv/api/User.html#user_GET>`_
        
        Args:
            fields (list, optional): 
                A list of attributes to return for each user.
        
        Returns:
            list: A list of user resources.
        
        Examples:
            >>> for user in nessus.users.list():
            ...     pprint(user)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) 
                for f in fields])

        return self._api.get('users', params=params).json()

    def create(self, username, password, permissions, 
            name=None, email=None, account_type=None):
        '''
        Create a new user.

        `users: create <https://cloud.tenable.com/api#/resources/users/create>`_

        Args:
            username (str): The username for the new user.
            password (str): The password for the new user.
            permissions (int): 
                The permissions role for the user.  The permissions integer 
                is derived based on the desired role of the user.  For details
                describing what permissions values mean what roles, please refer
                to the `User Roles <https://cloud.tenable.com/api#/authorization>`_
                table to see what permissions are accepted.
            name (str, optional): The human-readable name of the user.
            email (str, optional): The email address of the user.
            account_type (str, optional):
                The account type for the user.  The default is `local`.

        Returns:
            dict: The resource record of the new user.

        Examples:
            Create a standard user:

            >>> user = nessus.users.create('jsmith@company.com', 'password1', 32)

            Create an admin user and add the email and name:

            >>> user = nessus.create.users('jdoe@company.com', 'password', 64,
            ...     name='Jane Doe', email='jdoe@company.com')

        '''
        payload = {
            'username': self._check('username', username, str),
            'password': self._check('password', password, str),
            'permissions': self._check('permissions', permissions, int),
            'type': self._check('account_type', account_type, str, default='local'),
        }

        if name:
            payload['name'] = self._check('name', name, str)
        if email:
            payload['email'] = self._check('email', email, str)

        return self._api.post('users', json=payload).json()

    def delete(self, *user_ids):
        '''
        Removes a user from Nessus.

        `users: delete <https://cloud.tenable.com/api#/resources/users/delete>`_

        Args:
            id (int): The unique identifier of the user.

        Returns:
            None: The user was successfully deleted.

        Examples:
            >>> nessus.users.delete(1)
        '''
        if len(user_ids) <= 1:
            self._api.delete('users/{}'.format(
                self._check('id', user_ids, int)
            ))
        else:
            return self._api.delete('users',
                json={'ids': [self._check('id', i, int) for i in user_ids]}).json()
            
    def details(self, id):
        '''
        Retrieve the details of a user.

        `users: details <https://cloud.tenable.com/api#/resources/users/details>`_

        Args:
            id (int): THe unique identifier for the user.

        Returns:
            dict: The resource record for the user.

        Examples:
            >>> user = nessus.users.details(1)
        '''
        return self._api.get('users/{}'.format(self._check('id', id, int))).json()

    def edit(self, id, permissions=None, name=None, email=None, lockout=None):
        '''
        Modify an existing user.

        `users: edit <https://cloud.tenable.com/api#/resources/users/edit>`_

        Args:
            id (int): The unique identifier for the user.
            permissions (int, optional):
                The permissions role for the user.  The permissions integer 
                is derived based on the desired role of the user.  For details
                describing what permissions values mean what roles, please refer
                to the `User Roles <https://cloud.tenable.com/api#/authorization>`_
                table to see what permissions are accepted.
            name (str, optional): The human-readable name of the user.
            email (str, optional): The email address of the user.
            lockout (bool, optional): Is the user account lockedout?

        Returns:
            dict: The modified user resource record.

        Examples:
            >>> user = nessus.users.edit(1, name='New Full Name')
        '''
        payload = dict()

        if permissions:
            payload['permissions'] = self._check('permissions', permissions, int)
        if lockout is not None:
            payload['lockout'] = self._check('lockout', lockout, bool)
        if email:
            payload['email'] = self._check('email', email, str)
        if name:
            payload['name'] = self._check('name', name, str)

        # Merge the data that we build with the payload with the user details.
        user = self.details(self._check('id', id, int))
        payload = dict_merge({
            'permissions': user['permissions'],
            'lockout': user['lockout'],
            'email': user['email'],
            'name': user['name'],
        }, payload)
        return self._api.put('users/{}'.format(id), json=payload).json()

    def change_password(self, id, old_password, new_password):
        '''
        Change the password for a specific user.

        `users: password <https://cloud.tenable.com/api#/resources/users/password>`_

        Args:
            id (int): The unique identifier for the user.
            old_password (str): The current password.
            new_password (str): The new password.

        Returns:
            None: The password has been successfully changed.

        Examples:
            >>> nessus.users.change_password(1, 'old_pass', 'new_pass')
        '''
        self._api.put('users/{}/chpasswd'.format(self._check('id', id, int)), json={
            'password': self._check('new_password', new_password, str),
            'current_password': self._check('old_password', old_password, str)
        })

    def gen_api_keys(self, id):
        '''
        Generate the API keys for a specific user.

        `users: keys <https://cloud.tenable.com/api#/resources/user/keys>`_

        Args:
            id (int): The unique identifier for the user.

        Returns:
            dict: A dictionary containing the new API Key-pair.

        Examples:
            >>> keys = nessus.users.gen_api_keys(1)
        '''
        return self._api.put('users/{}/keys'.format(
            self._check('id', id, int))).json()