from .base import NessusEndpoint

class FoldersAPI(NessusEndpoint):
    def create(self, name):
        '''
        Create a folder.

        `folders: create </api#/resources/folders/create>`_

        Args:
            name (str):
                The name of the new folder.

        Returns:
            int: The new folder id.

        Examples:
            >>> folder = nessus.folders.create('New Folder Name')
        '''
        return self._api.post('folders', json={
            'name': self._check('name', name, str)
        }).json()['id']

    def delete(self, id):
        '''
        Delete a folder.

        `folders: delete </api#/resources/folders/delete>`_

        Args:
            id (int): The unique identifier for the folder.

        Returns:
            None

        Examples:
            >>> nessus.folders.delete(1)
        '''
        self._api.delete('folders/{}'.format(self._check('id', id, int)))

    def edit(self, id, name):
        '''
        Edit a folder.

        `folders: edit </api#/resources/folders/edit>`_

        Args:
            id (int): The unique identifier for the folder.
            name (str): The new name for the folder.

        Returns:
            None: The folder was successfully renamed.

        Examples:
            >>> nessus.folders.edit(1, 'Updated Folder Name')
        '''
        self._api.put('folders/{}'.format(self._check('id', id, int)), json={
            'name': self._check('name', name, str)
        })

    def list(self):
        '''
        Lists the available folders.

        `folders: list </api#/resources/folders/list>`_

        Returns:
            list: List of folder resource records.

        Examples:
            >>> for folder in nessus.folders.list():
            ...     pprint(folder)
        '''
        return self._api.get('folders').json()['folders']

