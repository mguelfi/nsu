'''
filters
=======

Tenable.io supplies the filters as a REST endpoint, for Nessus we recreate
a static scan_filters method rather than refactor a lot of code.

Methods available on ``nessus.filters``:

.. rst-class:: hide-signature
.. autoclass:: FiltersAPI

    .. automethod:: scan_filters
'''
from .base import NessusEndpoint

class FiltersAPI(NessusEndpoint):

    filters = {
        'plugin.attributes.bid':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '[0-9]+'},
        'xref:CERT':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '[0-9]+'},
        'plugin.attributes.cpe':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '.*'},
        'plugin.attributes.cve.raw':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': 'CVE-[0-9]{4}-.*'},
        'plugin.attributes.cvss_base_score':
            {'operators': 'lt, gt, eq, neq, match, nmatch', 'choices': None, 'pattern': '[0-9]+'},
        'plugin.attributes.cvss_temporal_score':
            {'operators': 'lt, gt, eq, neq, match, nmatch', 'choices': None, 'pattern': '[0-9]+'},
        'plugin.attributes.cvss_temporal_vector.raw':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '.*'},
        'plugin.attributes.cvss_vector.raw':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '.*'},
        'plugin.attributes.cvss3_base_score':
            {'operators': 'lt, gt, eq, neq, match, nmatch', 'choices': None, 'pattern': '[0-9]+'},
        'plugin.attributes.cvss3_temporal_score':
            {'operators': 'lt, gt, eq, neq, match, nmatch', 'choices': None, 'pattern': '[0-9]+'},
        'plugin.attributes.cvss3_temporal_vector.raw':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '.*'},
        'plugin.attributes.cvss3_vector.raw':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '.*'},
        'xref:CWE':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '[0-9]+'},
        'plugin.attributes.exploit_available':
            {'operators': 'eq, neq', 'choices': 'true, false', 'pattern': None},
        'plugin.attributes.exploitability_ease.raw':
            {'operators': 'eq, neq', 'choices': 'Exploits are available, No exploit is required, No known exploits are available', 'pattern': None},
        'plugin.attributes.exploited_by_malware':
            {'operators': 'eq, neq', 'choices': 'true, false', 'pattern': None},
        'plugin.attributes.exploited_by_nessus':
            {'operators': 'eq, neq', 'choices': 'true, false', 'pattern': None},
        'host.hostname':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '.*'},
        'xref:IAVA':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '[0-9]{4}-[AB]-.*'},
        'xref:IAVB':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '[0-9]{4}-[AB]-.*'},
        'plugin.attributes.stig_severity':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '.*'},
        'xref:IAVT':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '[0-9]{4}-[AB]-.*'},
        'plugin.attributes.in_the_news':
            {'operators': 'eq, neq', 'choices': 'true, false', 'pattern': None},
        'xref:MSFT':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': 'MS[0-9]{2}-[0-9]{3}'},
        'xref:OSVDB':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '[0-9]+'},
        'plugin.attributes.patch_publication_date':
            {'operators': 'date-lt, date-gt, date-eq, date-neq, match, nmatch', 'choices': None, 'pattern': '[0-9]{2}/[0-9]{2}/[0-9]{4}'},
        'plugin.attributes.description':
            {'operators': 'match, nmatch', 'choices': None, 'pattern': '.*'},
        'plugin.family':
            {'operators': 'eq, neq', 'choices': None, 'pattern': '.*'},
        'plugin.id':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '[0-9]+'},
        'plugin.attributes.plugin_modification_date':
            {'operators': 'date-lt, date-gt, date-eq, date-neq, match, nmatch', 'choices': None, 'pattern': '[0-9]{2}/[0-9]{2}/[0-9]{4}'},
        'plugin.name':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '.*'},
        'output':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '.*'},
        'plugin.attributes.plugin_publication_date':
            {'operators': 'date-lt, date-gt, date-eq, date-neq, match, nmatch', 'choices': None, 'pattern': '[0-9]{2}/[0-9]{2}/[0-9]{4}'},
        'plugin.attributes.plugin_type':
            {'operators': 'eq, neq', 'choices': 'local, remote', 'pattern': None},
        'port.port':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '[0-9]+'},
        'port.protocol':
            {'operators': 'eq, neq', 'choices': 'tcp, udp, icmp', 'pattern': None},
        'plugin.attributes.risk_factor':
            {'operators': 'eq, neq', 'choices': 'None, Low, Medium, High, Critical', 'pattern': None},
        'plugin.attributes.see_also':
            {'operators': 'eq, neq, match, nmatch', 'choices': None, 'pattern': '.*'},
        'severity':
            {'operators': 'eq, neq', 'choices': 'None, Low, Medium, High, Critical', 'pattern': None},
        'plugin.attributes.solution':
            {'operators': 'match, nmatch', 'choices': None, 'pattern': '.*'},
        'plugin.attributes.synopsis':
            {'operators': 'match, nmatch', 'choices': None, 'pattern': '.*'},
        'plugin.attributes.vuln_publication_date':
            {'operators': 'date-lt, date-gt, date-eq, date-neq, match, nmatch', 'choices': None, 'pattern': '[0-9]{2}/[0-9]{2}/[0-9]{4}'}
    }

    def scan_filters(self):
        return self.filters
