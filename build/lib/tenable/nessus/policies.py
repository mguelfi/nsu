'''
policies
========

The following methods allow for interaction into the Nessus
 `policies </api#/resources/policies>`_ API.

Methods available on ``nessus.policies``:

.. rst-class:: hide-signature
.. autoclass:: PoliciesAPI

    .. automethod:: configure
    .. automethod:: copy
    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: policy_import
    .. automethod:: policy_export
    .. automethod:: list
'''
from .base import NessusEndpoint
from tenable.utils import dict_merge, policy_settings
from io import BytesIO

class PoliciesAPI(NessusEndpoint):
    def templates(self):
        '''
        returns a dictionary of the scan policy templates using the
        format of dict['name'] = 'UUID'.  This is useful for being able to
        define scan policy templates w/o having to remember the UUID for each
        individual one.
        '''
        policies = dict()
        for item in self._api.editor.list('policy'):
            policies[item['name']] = item['uuid']
        return policies

    def template_details(self, name):
        '''
        Calls the editor API and parses the policy template config to return a
        document that closely matches what the API expects to be POSTed or PUTed
        via the policy create and configure methods.  The compliance audits and
        credentials are populated into the 'current' sub-document for the
        relevant resources.

        Args:
            name (str): The name of the scan .

        Returns:
            dict: The policy configuration resource.

        Examples:
            >>> template = tio.policies.template('basic')
            >>> pprint(template)

        Please note that template_details is reverse-engineered from the
        responses from the editor API and isn't guaranteed to work.
        '''

        # Get the policy template UUID
        tmpl = self.templates()
        tmpl_uuid = tmpl[self._check('name', name, str, choices=tmpl.keys())]

        # Get the editor object
        editor = self._api.get('editor/policy/templates/{}'.format(
            self._check('tmpl_uuid', tmpl_uuid, str))).json()

        # define the initial skeleton of the scan object
        scan = {
            'settings': policy_settings(editor['settings']),
            'uuid': editor['uuid']
        }

        # graft on the basic settings that aren't stored in any input sections.
        for item in editor['settings']['basic']['groups']:
            for setting in item.keys():
                if setting not in ['name', 'title', 'inputs']:
                    scan['settings'][setting] = item[setting]

        if 'credentials' in editor:
            # if the credentials sub-document exists, then lets walk down the
            # credentials dataset
            scan['credentials'] = {
                'current': self._api.editor.parse_creds(
                    editor['credentials']['data'])
            }

            # We also need to gather the settings from the various credential
            # settings that are unique to the scan.
            for ctype in editor['credentials']['data']:
                for citem in ctype['types']:
                    if 'settings' in citem and citem['settings']:
                        scan['settings'] = dict_merge(
                            scan['settings'], policy_settings(
                                citem['settings']))

        if 'compliance' in editor:
            # if the audits sub-document exists, then lets walk down the
            # audits dataset.
            scan['compliance'] = {
                'current': self._api.editor.parse_audits(
                    editor['compliance']['data'])
            }

            # We also need to add in the "compliance" settings into the scan
            # settings.
            for item in editor['compliance']['data']:
                if 'settings' in item:
                    scan['settings'] = dict_merge(
                        scan['settings'], policy_settings(
                            item['settings']))
        print(editor['plugins']['families'])
        if 'plugins' in editor:
            # if the plugins sub-document exists, then lets walk down the
            # plugins dataset.
            scan['plugins'] = self._api.editor.parse_plugins(
                editor['plugins']['families'], tmpl_uuid)

        return scan

    def configure(self, policy_id, policy):
        '''
        Configures an existing policy.

        `policies: configure </api#/resources/policies/configure>`_

        Args:
            id (int): The policy unique identifier.
            policy (dict):
                The updated policy definition to push into Nessus.  As these
                policies can be quite complex, please refer to the documentation
                in the policies: configure page (linked above).

        Returns:
            None: Policy successfully modified.

        Examples:
            >>> policy = nessus.policies.details(1)
            >>> policy['settings']['name'] = 'Updated Policy Name'
            >>> nessus.policies.configure(policy)
        '''
        self._api.put('policies/{}'.format(self._check('policy_id',
                                                       policy_id, int)),
                      json=self._check('policy', policy, dict))

    def copy(self, policy_id):
        '''
        Duplicates a scan policy and returns the copy.

        `policies: copy </api#/resources/policies/copy>`_

        Args:
            id (int): The unique identifier of the policy you wish to copy.

        Returns:
            dict: A dictionary containing the name and id of the policy copy.

        Example:
            >>> policy = nessus.policies.copy(1)
        '''
        return self._api.post('policies/{}/copy'.format(
            self._check('policy_id', policy_id, int))).json()

    def create(self, policy):
        '''
        Creates a new scan policy based on the policy dictionary passed.

        `policies: configure </api#/resources/policies/configure>`_

        Args:
            policy (dict):
                The policy definition to push into Nessus.  As these
                policies can be quite complex, please refer to the documentation
                in the policies: configure page (linked above).

        Returns:
            dict: A dictionary containing the name and id of the new policy.

        Examples:
            >>> policy = nessus.policies.template_details('basic')
            >>> policy['settings']['name'] = 'New Scan Policy'
            >>> info = nessus.policies.create(policy)
        '''
        return self._api.post('policies',
                              json=self._check('policy', policy, dict)).json()

    def delete(self, *policy_ids):
        '''
        Delete a custom policy.

        `policies: delete </api#/resources/policies/delete>`_

        Args:
            id (int): The unique identifier of the policy to delete.

        Returns:
            None: The policy was successfully deleted.

        Examples:
            >>> nessus.policies.delete(1)
        '''
        if len(policy_ids) <= 1:
            self._api.delete('policies/{}'.format(
                self._check('policy_ids', policy_ids, int)
            ))
        else:
            self._api.delete('policies',
                             json={'ids': [self._check('policy_ids', i, int) for i in policy_ids]})


    def details(self, policy_ids):
        '''
        Retrieve the details for a specific policy.

        `policies: details </api#/resources/policies/details>`_

        Args:
            id (int): The unique identifier of the policy.

        Returns:
            dict: The dictionary definition of the policy.

        Examples:
            >>> policy = nessus.policies.details(1)
        '''
        return self._api.get('policies/{}'.format(
            self._check('policy_ids', policy_ids, int))).json()

    def policy_import(self, fobj):
        '''
        Imports a policy into Nessus.

        `policies: import </api#/resources/policies/import>`_

        Args:
            fobj (FileObject):
                The file object of the scan policy you wish to import.

        Returns:
            dict: The dictionary of the imported policy.

        Examples:
            >>> with open('example.nessus') as policy:
            ...     nessus.policies.import(policy)
        '''
        fid = self._api.files.upload(fobj)
        return self._api.post('policies/import', json={'file': fid}).json()

    def policy_export(self, policy_id, fobj=None):
        '''
        Exports a specified policy from Nessus.

        `policies: export </api#/resources/policies/export>`_

        Args:
            id (int): The unique identifier of the policy to export.
            fobj (FileObject, optional):
                A file-like object to write the contents of the policy to.  If
                none is provided a BytesIO object will be returned with the
                policy.

        Returns:
            FileObject: A file-like object containing the contents of the policy
            in XML format.

        Examples:
            >>> with open('example.nessus', 'wb') as policy:
            ...     nessus.policies.export(1, policy)
        '''
        # If no file object was givent to us, then lets create a new BytesIO
        # object to dump the data into.
        if not fobj:
            fobj = BytesIO()

        # make the call to get the file.
        resp = self._api.get('policies/{}/export'.format(
            self._check('policy_id', policy_id, int)), stream=True)

        # Stream the data into the file.
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)

        # return the FileObject.
        return fobj

    def list(self):
        '''
        List the available custom policies.

        `policies: list </api#/resources/policies/list>`_

        Returns:
            list: List of policy resource documents.

        Examples:
            >>> for policy in nessus.policies.list():
            ...     pprint(policy)
        '''
        return self._api.get('policies').json()['policies']
