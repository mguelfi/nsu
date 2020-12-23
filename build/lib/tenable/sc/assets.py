from .base import SCEndpoint
import re
from ipaddress import IPv4Address, IPv4Network, summarize_address_range, \
    AddressValueError

class AssetsAPI(SCEndpoint):
    def ip_list_to_list(self, ip_list):
        '''
        Returns a list of IPs from Security Center's string representation
        
        Args:
            ip_list (str):
                is either comma or newline separated and can include:
                    bare ip: 192.168.1.1
                    cidr notation: 192.168.1.2/31
                    ranges: 192.168.1.3-192.168.3.4

        Returns:
            list: list of IPs (str)
        '''
        ip_list = re.split(',|\n', ip_list)
        
        result = []
        for entry in ip_list:
            result += self.enum_ips(entry)
        return result
    
    def enum_ips(self, ip_string):
        '''
        Expands 'ranges' into IPs
        
        Args:
            ip_string (str):
                bare ip: 192.168.1.1
                cidr notation: 192.168.1.2/31
                ranges: 192.168.1.3-192.168.3.4

        Returns:
            list: list of IP strings
        '''
        result = []
        try:
            ip_string = unicode(ip_string)  #Python2
        except NameError:
            pass                            #Python3
        
        try:
            # just an IP
            result = [str(IPv4Address(ip_string))]
        except AddressValueError:
            try:
                # CIDR notation
                result = [str(ip) for ip in IPv4Network(ip_string)]
            except AddressValueError:
                try:
                    # IP Address range
                    start, end = ip_string.split('-')
                    network_list = [ip for ip in summarize_address_range(
                            IPv4Address(start),
                            IPv4Address(end))]
                    result = []
                    for network in network_list:
                        for ip in network:
                            result.append(str(ip))
                except:
                    pass
        return result

    def list(self, fields=None):
        '''
        Returns a list of assets.

        `assets: list-assets <https://cloud.tenable.com/api#/resources/assets/list-assets>`_

        Args:
            fields (list, optional): A list of attributes to return.

        Returns:
            list: List of asset records.

        Examples:
            >>> for asset in sc.assets.list():
            ...     pprint(asset)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])
        return self._api.get('asset', params=params).json()['response']

    def details(self, asset_id):
        '''
        Retrieves the details about a specific asset.

        `assets: asset-info <https://cloud.tenable.com/api#/resources/assets/asset-info>`_

        Args:
            uuid (str):
                The UUID (unique identifier) for the asset.

        Returns:
            dict: Asset resource definition.

        Examples:
            >>> asset = sc.assets.details('00000000-0000-0000-0000-000000000000')
        '''
        return self._api.get(
            'asset/{}'.format(
                self._check('asset_id', asset_id, int)
            )).json()['response']

    def patch(self, asset_id, patch):
        '''
        Applies a patch to an asset
        
        The patch is expected in the same format as the details output.
        
        Args:
            asset_id (int): the asset id
            patch (dict): a dict of values to patch
                e.g. {'definedIPs':'10.0.0.0,192.168.0.1'}
        
        Returns:
            dict: the asset resource record
        '''
        
        return self._api.patch('asset/{}'.format(
                   self._check('asset_id', asset_id, int)),
                       json=patch).json()['response']

    def create(self, asset_details):
        '''
        Creates an asset from the output of an assets.details() call.

        Args:
            asset_details (dict): the asset description

        Returns:
            dict: the asset resource record
        '''
        return self._api.post('asset', json=asset_details).json()['response']

