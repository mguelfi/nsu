'''
agent scans
===========

The following methods allow for interaction into the Tenable.sc
`Agent Results Sync <https://docs.tenable.com/sccv/api/Agent-Results-Sync.html>`_ API.
While these endpoints are under /agentResultSync they appear in Tenable.sc
in the **Agent Scans** section.

Methods available on ``sc.agent_scans``:

.. rst-class:: hide-signature
.. autoclass:: AgentScanAPI

    .. automethod:: copy
    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
    .. automethod:: sync
'''

from .base import SCEndpoint

class AgentScanAPI(SCEndpoint):
    def _constructor(self, **kw):
        '''
        Handles parsing the keywords and returns a scan definition document
        '''
        if 'name' in kw:
            self._check('name', kw['name'], str)

        if 'repo' in kw:
            # as we accept input as a integer, we need to expand the repository
            # attribute to be a dictionary item with just the ID (per API docs)
            kw['repository'] = {'id': self._check(
                'repo', kw['repo'], int)}
            del(kw['repo'])

        if 'nessus_manager' in kw:
            # As per repo, create a dict
            kw['nessusManager'] = {'id': self._check(
                'nessus_manager', kw['nessus_manager'], int)}
            del(kw['nessus_manager'])

        if 'type' in kw:
            self._check('type', kw['type'], str, choices=['plugin', 'policy'])

        if 'description' in kw:
            self._check('description', kw['description'], str)

        if 'scans_glob' in kw:
            kw['scansGlob'] = self._check('scans_glob', kw['scans_glob'], str)
            del(kw['scans_glob'])

        if 'email_complete' in kw:
            # As emailOnFinish is effectively a string interpretation of a bool
            # value, if the snake case equivalent is used, we will convert it
            # into the expected parameter and remove the snake cased version.
            kw['emailOnFinish'] = str(self._check(
                'email_complete', kw['email_complete'], bool)).lower()
            del(kw['email_complete'])

        if 'email_launch' in kw:
            # As emailOnLaunch is effectively a string interpretation of a bool
            # value, if the snake case equivalent is used, we will convert it
            # into the expected parameter and remove the snake cased version.
            kw['emailOnLaunch'] = str(self._check(
                'email_launch', kw['email_launch'], bool)).lower()
            del(kw['email_launch'])

        if 'dhcp_tracking' in kw:
            # convert bool => str
            kw['dhcpTracking'] = str(self._check(
                'dhcp_tracking', kw['dhcp_tracking'], bool)).lower()
            del(kw['dhcp_tracking'])
            
        # hand off the building the schedule sub-document to the schedule 
        # document builder.
        if 'schedule' in kw:
            kw['schedule'] = self._schedule_constructor(kw['schedule'])

        if 'reports' in kw:
            # as the reports list should already be in a format that the API
            # expects, we will simply verify that everything looks like it should.
            for item in self._check('reports', kw['reports'], list):
                self._check('report:id', item['id'], int),
                self._check('reportSource', item['reportSource'], str, choices=[
                    'cumulative', 
                    'patched', 
                    'individual', 
                    'lce', 
                    'archive', 
                    'mobile'
                ])

        return kw

    def list(self, fields=None):
        '''
        Retrieves the list of Agent Scan definitions
        
        + `SC Agent Scan List <https://docs.tenable.com/sccv/api/Agent-Results-Sync.html#agentResultsSync_GET>`_
        
        Args:
            fields (list, optional):
                A list of attributes to return for each agent scan

        Returns:
            list: A list of scan resources

        Examples:
            >>> for scan in sc.agent_scans.list():
            ...     pprint(scan)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                for f in fields])

        return self._api.get('agentResultsSync', params=params).json()['response']

    def create(self, name, repo, nessus_manager, **kw):
        '''
        Creates an Agent Scan definition.

        + `SC Agent Scan Create <https://docs.tenable.com/sccv/api/Agent-Results-Sync.html#agentResultsSync_POST>`_

        Args:
            name (str): The name of the scan.
            repo (int):
                The target repository id for the scan.
            description (str, optional): A description for the scan.
            nessus_manager (int): scanner id
            scans_glob (str, optional):
                pattern to match scan names
                default '*'
            dhcp_tracking (bool, optional):
                Should DHCP host tracking be enabled?
                The default ``False``
            schedule (dict, optional):
                A dictionary detailing the repeating schedule of the scan.  
                For more information refer to `Schedule Dictionaries`_
            download_results_after: (int, optional):
                A valid unix timestamp
                The default is ``-1``
            reports (list, optional):
                What reports should be run upon completion of the scan?  Each
                report dictionary requires an id for the report definition and
                the source for which to run the report against.  Example:
                ``{'id': 1, 'reportSource': 'individual'}``.
                The default is ``[]``
            email_launch: (bool, optional):
                Send an e-mail notifying you when the scan has launched?
                The default is ``False``.
            email_complete: (bool, optional):
                Send an e-mail notifying you when the scan has finished?
                The default is ``False``

        Returns:
            dict: The scan resource for the created agent scan.

        Examples:
            Create a scan for desktops:

            >>> sc.agent_scans.create('Desktop Scans', 1, 1,
            ...     scans_glob='*desktop*')
        '''
        kw['name'] = name
        kw['repo'] = repo
        scan = self._constructor(**kw)

        return self._api.post('agentResultsSync', json=scan).json()['response']

    def details(self, id, fields=None):
        '''
        Returns the details for a specific agent scan.

        + `SC Agent Scan Create <https://docs.tenable.com/sccv/api/Agent-Results-Sync.html#agentResultsSync_id_GET>`_

        Args:
            id (int): The identifier for the scan.
            fields (list, optional): A list of attributes to return.

        Returns:
            dict: the scan resource record.

        Examples:
            >>> agent_scan = sc.agent_scans.detail(1)
            >>> pprint(agent_scan)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('agentResultsSync/{}'.format(self._check('id', id, int)),
                             params=params).json()['response']
        
    def edit(self, id, **kw):
        '''
        Edits an existing agent scan definition.
        
        + `SC Agent Scan Create <https://docs.tenable.com/sccv/api/Agent-Results-Sync.html#agentResultsSync_id_PATCH>`_

        Args:
            id (int): The identifier for the scan.
            name (str, optional): The name of the scan.
            repo (int, optional):
                The target repository id for the scan.
            description (str, optional): A description for the scan.
            nessus_manager (int, optional): scanner id
            scans_glob (str, optional):
                pattern to match scan names
                default '*'
            dhcp_tracking (bool, optional):
                Should DHCP host tracking be enabled?
                The default ``False``
            schedule (dict, optional):
                A dictionary detailing the repeating schedule of the scan.  
                For more information refer to `Schedule Dictionaries`_
            reports (list, optional):
                What reports should be run upon completion of the scan?  Each
                report dictionary requires an id for the report definition and
                the source for which to run the report against.  Example:
                ``{'id': 1, 'reportSource': 'individual'}``.
                The default is ``[]``
            email_launch: (bool, optional):
                Send an e-mail notifying you when the scan has launched?
                The default is ``False``.
            email_complete: (bool, optional):
                Send an e-mail notifying you when the scan has finished?
                The default is ``False``
                
        Returns:
            dict: The agent scan resource for the updated agent scan.

        Examples:
            >>> sc.agent_scans.edit(1, name='Windows desktop scan')
        '''
        scan = self._constructor(**kw)
        return self._api.patch('agentResultsSync/{}'.format(self._check('id', id, int)), 
                               json=scan).json()['response']

    def delete(self, id):
        '''
        Removes the specified agent scan from SecurityCenter.

        + `SC Agent Scan Create <https://docs.tenable.com/sccv/api/Agent-Results-Sync.html#agentResultsSync_id_DELETE>`_

        Args:
            id (int): The identifier for the agent scan to delete.

        Examples:
            >>> sc.agent_scans.delete(1)
        '''
        self._api.delete('agentResultsSync/{}'.format(self._check('id', id, int)))
        
    def copy(self, id, name, user_id):
        '''
        Copies an existing scan definition.

        + `SC Agent Scan Create <https://docs.tenable.com/sccv/api/Agent-Results-Sync.html#agentResultsSyncCopyPOST1>`_

        Args:
            id (int): The agent scan definition identifier to copy.
            name (str): The name of the copy thats created.
            user_id (int): 
                The user id to assign as the owner of the new agent scan.

        Returns:
            dict: Scan definition resource.

        Examples:
            >>> sc.agent_scans.copy(1, name='Cloned Scan', 1)
        '''
        payload = {
            'name': self._check('name', name, str),
            'targetUser': {'id': self._check('user_id', user_id, int)}
        }

        return self._api.post('agentResultsSync/{}/copy'.format(
            self._check('id', id, int)), json=payload).json()['response']['resultsSync']

    def sync(self, id):
        '''
        Launches an Agent Scan Sync

        + `SC Agent Scan Create <https://docs.tenable.com/sccv/api/Agent-Results-Sync.html#AgentResultsSyncRESTReference-/agentResultsSync/{id}/launch>`_

        Args:
            id (int): The agent scan defintion to sync

        Returns:
            dict: Agent scan results resource for the sync

        Examples:
            >>> running = sc.agent_scans.sync(1)
            >>> print('The Agent Scan Result ID is {}'.format(
            ...     running['resultsSyncID']))
        '''

        return self._api.post('agentResultsSync/{}/launch'.format(
                self._check('id', id, int))).json()['response']
