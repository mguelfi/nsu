from .base import SCEndpoint

class DashboardAPI(SCEndpoint):

    def list(self, filter=None):
        '''
        Retrieves the list of dashboards

        Args:
            filters (str, optional): 
                activated, usable, manageable

        Returns:
            dict: A list of dashbaords.

        Examples:
            >>> for dashboard in sc.dashboard.list():
            ...     print(dashboard)
        '''
        params = dict()
        if filter:
            params['filter'] = filter

        return self._api.get('dashboard', params=params).json()['response']

    def details(self, dashboard_id):
        '''
        Retrieves the dashboard
        
        Args:
            dashboard_id (int)
            
        Returns:
            dict: a dashboard
                keys() are ['id', 'name', 'description', 'numColumns',
                'columnWidths', 'defaultTemplateNumber', 'createdTime',
                'modifiedTime', 'order', 'activated', 'dashboardComponents',
                'groups', 'failedComponentCount', 'canUse', 'canManage',
                'owner', 'ownerGroup', 'targetGroup']
            
        Examples:
            >>> sc.dashboard.details(1):
        '''
        return self._api.get('dashboard/{}/component'.format(
            self._check('dashboard_id', dashboard_id, int))).json()['response']
    
    def components(self, dashboard_id, component_id):
        '''
        Retrieves the dashboard component
        
        Args:
            dashboard_id (int)
            component_id (int)
            
        Returns:
            dict: the component
                keys() are ['id', 'name', 'description', 'tabID',
                'componentType', 'column', 'order', 'status', 'running',
                'lastUpdatedTime', 'lastCompletedUpdateTime', 'createdTime',
                'modifiedTime', 'definition', 'schedule', 'data',
                'queryStatus']
            
        Examples:
            >>> sc.dashboard.components(1, 3):
        '''
        return self._api.get('dashboard/{}/component/{}'.format(
            self._check('dashboard_id', dashboard_id, int),
            self._check('component_id', component_id, int))).json()['response']
