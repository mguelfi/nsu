'''
system
======

The following methods allow for interaction into the Nessus
 `Server </api#/resources/server>`_ API. 

Methods available on ``nessus.system``:

.. rst-class:: hide-signature
.. autoclass:: SystemAPI

    .. automethod:: details
'''
from .base import NessusEndpoint

class SystemAPI(NessusEndpoint):
    def details(self):
        '''
        Retrieves information about the Nessus instance.  This method should
        only be called before authentication has occurred.  As most of the
        information within this call already happens upon instantiation, there
        should be little need to call this manually.

        Returns:
            dict: The response dictionary
        
        Examples:
            >>> info = nessus.system.details()
        '''
        return self._api.get('server/properties').json()

