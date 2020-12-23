from .base import NessusEndpoint

class PluginsAPI(NessusEndpoint):
    def families(self):
        '''
        List the available plugin families.

        `plugins: families </api#/resources/plugins/families>`_

        Returns:
            list: List of plugin familiy resource records.

        Examples:
            >>> for family in nessus.plugins.families():
            ...     pprint(family)
        '''
        return self._api.get('plugins/families').json()['families']

    def family_details(self, id):
        '''
        Retrieve the details for a specific plugin family.

        `plugins: family-details </api#/resources/plugins/family-details>`_

        Args:
            id (int): The plugin family unique identifier.

        Returns:
            dict: 
                Returns a dictionary stating the id, name, and plugins that are
                housed within the plugin family.

        Examples:
            >>> family = nessus.plugins.family_details(1)
        '''
        return self._api.get('plugins/families/{}'.format(
                self._check('id', id, int)
        )).json()

    def plugin_details(self, id):
            '''
            Retrieve the details for a specific plugin.

            `plugins: plugin-details </api#/resources/plugins/plugin-details>`_

            Args:
                id (int): The plugin id for the requested plugin.

            Returns:
                dict:
                    A dictionary stating the id, name, family, and any other
                    relevant attributes associated to the plugin.

            Examples:
                >>> plugin = nessus.plugins.plugin_details(19506)
                >>> pprint(plugin)
            '''
            return self._api.get('plugins/plugin/{}'.format(
                self._check('id', id, int))).json()

