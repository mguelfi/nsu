from tenable.base import APISession
from tenable.errors import *
from .agents import AgentsAPI
from .agent_groups import AgentGroupsAPI
from .editor import EditorAPI
from .files import FileAPI
from .filters import FiltersAPI
from .folders import FoldersAPI
from .groups import GroupsAPI
from .permissions import PermissionsAPI
from .plugins import PluginsAPI
from .policies import PoliciesAPI
from .scanners import ScannersAPI
from .scans import ScansAPI
from .status import StatusAPI
from .system import SystemAPI
from .users import UserAPI


import warnings, logging


class Nessus(APISession):
    '''Nessus API Wrapper

    Args:
        host (str):
            The address of the Nessus instance to connect to.
        adapter (requests.Adaptor, optional):
            If a requests session adaptor is needed to ensure connectivity
            to the Nessus host, one can be provided here.
        backoff (float, optional):
            If a 429 response is returned, how much do we want to backoff
            if the response didn't send a Retry-After header.  The default
            backoff is ``1`` second.
        cert (tuple, optional):
            The client-side SSL certificate to use for authentication.  This
            format could be either a tuple or a string pointing to the
            certificate.  For more details, please refer to the 
            `Requests Client-Side Certificates`_ documentation.
        port (int, optional):
            The port number to connect to on the specified host.  The
            default is port ``443``.
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is ``3``.
        scheme (str, optional):
            What HTTP scheme should be used for URI path construction.  The
            default is ``https``.
        session (requests.Session, optional):
            If a requests Session is provided, the provided session will be used
            instead of constructing one during initialization.
        ssl_verify (bool, optional): 
            Should the SSL certificate on the Nessus instance be verified?
            Default is False.
        ua_identity (str, optional):
            An application identifier to be added into the User-Agent string
            for the purposes of application identification.
        

    Examples:
        A direct connection to Nessus:

        >>> from nessus import Nessus
        >>> nessus = Nessus('nessus.company.tld')

        A connection to Nessus using SSL certificates:

        >>> nessus = Nessus('nessus.company.tld', 
        ...     cert=('/path/client.cert', '/path/client.key'))

        Using an adaptor to use a passworded certificate (via the immensely 
        useful `requests_pkcs12`_ adaptor):

        >>> from requests_pkcs12 import Pkcs12Adapter
        >>> adapter = Pkcs12Adapter(
        ...     pkcs12_filename='certificate.p12', 
        ...     pkcs12_password='omgwtfbbq!')
        >>> nessus = Nessus('securitycenter.company.tld', adapter=adapter)
    

    '''
    _restricted_paths = ['token']
    _error_codes = {
        400: InvalidInputError,
        403: APIError,
        404: NotFoundError,
        500: ServerError,
    }

    def __init__(self, host, port=443, ssl_verify=False, cert=None, adapter=None,
                 scheme='https', retries=None, backoff=None, ua_identity=None,
                 session=None, proxies=None, access_key=None, secret_key=None):
        # As we will always be passing a URL to the APISession class, we will
        # want to construct a URL that APISession (and further requests) 
        # understands.
        base = '{}://{}:{}'.format(scheme, host, port)
        url = '{}'.format(base)

        # Now lets pass the relevent parts off to the APISession's constructor
        # to make sure we have everything lined up as we expect.
        APISession.__init__(self, url, 
            retries=retries, 
            backoff=backoff, 
            ua_identity=ua_identity, 
            session=session,
            proxies=proxies)

        # Also, as Nessus is generally installed without a certificate
        # chain that we can validate, we will want to turn off verification 
        # and the associated warnings unless told to otherwise:
        self._session.verify = ssl_verify
        if not ssl_verify:
            warnings.filterwarnings('ignore', 'Unverified HTTPS request')

        # If a client-side certificate is specified, then we will want to add
        # it into the session object as well.  The cert parameter is expecting
        # a path pointing to the client certificate file.
        if cert:
            self._session.cert = cert

        # If an adapter for requests was provided, we should pull that in as
        # well.
        if adapter:
            self._session.mount(base, adapter)

        # We will attempt to make the first call to the Nessus instance
        # and get the system information.  If this call fails, then we likely
        # aren't pointing to Nessus at all and should throw an error
        # stating this.
        try:
            self.info = self.system.details()
        except:
            raise
            raise ConnectionError('No Nessus Instance at {}:{}'.format(host, port))

        if access_key and secret_key:
            keys = 'accessKey={}; secretKey={}'.format(access_key, secret_key)
            self._session.headers.update({'X-ApiKeys': keys})

        # Now we will try to interpret the Nessus information into
        # something usable.
        try:
            self.version = self.info['server_version']
            self.build_id = self.info['server_build']
            self.type = self.info['nessus_type']
        except:
            raise


    @property
    def accept_risks(self):
        return AcceptRiskAPI(self)

    @property
    def agent_groups(self):
        return AgentGroupsAPI(self)

    @property
    def agents(self):
        return AgentsAPI(self)
    
    @property
    def alerts(self):
        return AlertAPI(self)

    @property
    def analysis(self):
        return AnalysisAPI(self)

    @property
    def editor(self):
        return EditorAPI(self)
    
    @property
    def feeds(self):
        return FeedAPI(self)

    @property
    def files(self):
        return FileAPI(self)

    @property
    def filters(self):
        return FiltersAPI(self)
    
    @property
    def folders(self):
        return FoldersAPI(self)

    @property
    def groups(self):
        return GroupsAPI(self)
    
    @property
    def permissions(self):
        return PermissionsAPI(self)
    
    @property
    def plugins(self):
        return PluginsAPI(self)
    
    @property
    def policies(self):
        return PoliciesAPI(self)
    
    @property
    def recast_risks(self):
        return RecastRiskAPI(self)
    
    @property
    def repositories(self):
        return RepositoryAPI(self)
    
    @property
    def roles(self):
        return RoleAPI(self)
    
    @property
    def scanners(self):
        return ScannersAPI(self)

    @property
    def scans(self):
        return ScansAPI(self)

    @property
    def scan_zones(self):
        return ScanZoneAPI(self)
    
    @property
    def status(self):
        return StatusAPI(self)
    
    @property
    def system(self):
        return SystemAPI(self)
    
    @property
    def users(self):
        return UserAPI(self)
