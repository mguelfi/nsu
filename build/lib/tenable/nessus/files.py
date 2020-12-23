from .base import NessusEndpoint
import uuid

class FileAPI(NessusEndpoint):
    def upload(self, fobj, encrypted=False):
        '''
        Uploads a file into Nessus.

        `file: upload <https://cloud.tenable.com/api#/resources/file/upload>`_

        Args:
            fobj (FileObject):
                The file object intended to be uploaded into Nessus.
            encrypted (bool, optional):
                If the file is encrypted, set the flag to True.

        Returns:
            str: The fileuploaded attribute

        Examples:
            >>> with open('file.txt') as fobj:
            ...     file_id = nessus.files.upload(fobj)
        '''

        # We will attempt to discover the name of the file stored within the
        # file object.  If none exists however, we will generate a random
        # uuid string to use instead.
        kw = dict()
        if encrypted:
            kw['data'] = {'no_enc': int(encrypted)}
        kw['files'] = {'Filedata': fobj}

        return self._api.post('file/upload', **kw).json()['fileuploaded']

