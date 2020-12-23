'''
status
======

The following methods allow for interaction into the Nessus
 `Status </api#/resources/server/status>`_ API.

Methods available on ``nessus.status``:

.. rst-class:: hide-signature
.. autoclass:: StatusAPI

    .. automethod:: status
'''
from .base import NessusEndpoint

class StatusAPI(NessusEndpoint):

    def status(self):
        return self._api.get('server/status').json()