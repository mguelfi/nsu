#!/usr/bin/env python3
import sys
import argparse
import configparser
import os
import os.path
import platform
import collections
import logging
import requests
import gzip
import distutils.util
from time import sleep
from tempfile import TemporaryFile
from tenable.nessus import Nessus
try:
    from azure.storage.fileshare import ShareFileClient
    from azure.storage.blob import BlobServiceClient
    import azure.core.exceptions
except ModuleNotFoundError:
    _no_azure_found = True

def main(method):
    """
    Collect scans from Nessus Manager and post them to Azure storage
    """
    nessus = connect_to_nessus()
    # Select the upload function, preference is file, fallback is blob
    if method == 'azure':
        if args.folder:
            _upload = file_upload
        else:
            _upload = blob_upload
    elif method == 'aws':
        _upload = put_upload
    # Collect new scan/history ids from Nessus
    scans, lastread = find_scans(nessus)

    for item in lastread:
        for scan in scans[item]:
            # Export the scan to a temp file
            with TemporaryFile() as fp:
                scan_name = str(item) + '_' + str(scan) + '.nessus'
                nessus.scans.export(int(item), history_id=int(scan), fobj=fp)
                fp.seek(0)
                # Upload the temp file to blob storage
                log.info('Posting {}'.format(scan_name))
                try:
                    _upload(fp, scan_name)
                except azure.core.exceptions.ClientAuthenticationError:
                    log.error('Authentication failed, check your connection string')
                    sys.exit(2)
                except requests.exceptions.HTTPError:
                    log.error('Authentication failed, check your AWS configuration')
                    sys.exit(3)
            log.debug('Sleeping for 30 seconds.')
            sleep(30)
        update_save(item, lastread[item], args.savefile)

def put_upload(fp, scan_name):
    """
    Uploads the contents of a file-like object as a PUT to an AWS API

    :param fp:
        file-like object to upload
    :param scan_name:
        str the name assigned to the object on the upload server
    """
    url = '{}/{}/{}'.format(args.aws_url, args.repo, scan_name)
    headers = {'x-api-key': args.api_key, 'content-encoding': 'gzip'}
    ssl_verify = bool(distutils.util.strtobool(args.aws['ssl_verify']))
    with TemporaryFile() as gzf:
        gzip.GzipFile(fileobj=gzf, mode='wb').write(fp.read())
        gzf.seek(0)
        r = requests.put(url, data=gzf, headers=headers, verify=ssl_verify)
    r.raise_for_status()

def file_upload(fp, scan_name):
    """
    Uploads the contents of a file-like object as file using the credentials
    in the configuration into the folder in the configuration.

    :param fp:
        file-like object to upload
    :param scan_name:
        str the name assigned to the object on the upload server
    """
    file_client = ShareFileClient.from_connection_string(
            args.conn_str, args.folder, scan_name)
    file_client.upload_file(fp)


def blob_upload(fp, scan_name):
    """
    Uploads the contents of a file-like object as a named blob using the
    credentials in the configuration into the container in the configuration.

    :param fp: 
        file-like object to upload
    :param scan_name:
        str the name assigned to the object on the upload server
    """
    blob_service_client = BlobServiceClient.from_connection_string(args.conn_str)
    blob_client = blob_service_client.get_blob_client(
            container=args.container, blob=scan_name)
    blob_client.upload_blob(fp)


def connect_to_nessus():
    """
    Connect to Nessus using the credentials collected from configuration/command line

    :returns: Nessus() connection
    """
    log.debug('Connecting to Nessus at: {}'.format(args.nessus['host']))
    ssl_verify = bool(distutils.util.strtobool(args.nessus['ssl_verify']))
    nessus = Nessus(args.nessus['host'],
            port=args.nessus['port'],
            ssl_verify=ssl_verify,
            access_key=args.access_key,
            secret_key=args.secret_key)
    info = nessus.info
    log.debug('Connected to: {}, version: {}.'.format(
        info.get('nessus_type', 'unknown'),
        info.get('server_version', 'unknown')))
    return nessus


def update_save(scan_id, last_modification_date, save_filename):
    """
    Update the save file with the last_modification_date for this scan.
    Needs to be called after each scan is processed to avoid double
    processing if there is an error in a later scan.

    :param scan_id:
        int the scan just processed
    :param last_modification_date:
        int date in epoch format that the last scan was completed
    :param save_filename:
        str filename per the configuration file
    """
    log = logging.getLogger(__name__)
    savefile = configparser.ConfigParser()
    try:
        savefile.read_file(open(save_filename))
        _ = savefile['lastread']
    except (FileNotFoundError, KeyError):
        savefile['lastread'] = {}
    log.debug('Updated scan {} with date: {}'.format(
        scan_id, last_modification_date))
    savefile['lastread'][str(scan_id)] = str(last_modification_date)
    with open(save_filename, 'w') as fh:
        savefile.write(fh)


def find_scans(nessus):
    """
    Collect all the scan results to pull.
    Each scan result must be 'completed' and created after the last one
    processed in the previous run.

    :param nessus:
        Nessus() API connection

    :returns: tuple (scans, lastread)
        where
        defaultdict(list) scans contains a list of history_ids per scan_id
        dict listread contains the last_modification_date per scan_id 
    """
    log = logging.getLogger(__name__)
    scans = collections.defaultdict(list)
    lastread = {} # dictionary of scan_id,last_modification_date for save config
    count = 0
    for scan in nessus.scans.list():
        try:
            history = sorted(nessus.scans.results(scan['id'])['history'],
                    key = lambda item: item['last_modification_date'])
            log.debug('Scan "{}" history size: {}'.format(scan['name'],
                len(history)))
            # sort by modification date so that the last entry is the latest scan
            lastread[scan['id']] = history[-1]['last_modification_date']
            for result in history:
                if (result['status'] == 'completed'
                        and (not args.lastread # empty save file
                            or result['last_modification_date'] >
                            int(args.lastread.get(str(scan['id']), 0)))):
                    scans[scan['id']].append(result['history_id'])
                    count += 1
        except TypeError: # scan has no history
            pass
    log.info('Found {} new scans.'.format(count))
    return scans, lastread

def load_config(path):
    """
    Loads configuration from file.

    :param path:
        path to config file. If not specified, several sensible
        default locations are tried depending on platform.

    :returns: ConfigParser() 'dict'
    """
    CONFIG_FILES = ["~/nessusScanUpload.conf"]

    if platform.system() == "Linux":
        CONFIG_FILES.extend(["/etc/nessusScanUpload.conf", "~/.nessusScanUpload"])
    elif platform.system() == "Windows" or platform.python_implementation() == "IronPython":
        CONFIG_FILES.extend(["nessusScanUpload.ini",
            os.path.join(os.getenv("APPDATA", ""), "nessusScanUpload.ini")])

    config = configparser.ConfigParser()
    if path is None:
        config.read([os.path.expanduser(path) for path in CONFIG_FILES])
    else:
        config.read(path)

    return config


def highlight(msg):
    print('==============================================================================')
    print('==============================================================================')
    print(msg)
    print('==============================================================================')
    print('==============================================================================')

def parse_argv():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file', '-c', dest='configfile',
            help='Configuration file to use')
    parser.add_argument('--save-file', dest='savefile', help='Path to save file,'
            ' overrides path in config file')
    parser.add_argument('--access-key', dest='access_key', help='Access Key for Nessus')
    parser.add_argument('--secret-key', dest='secret_key', help='Secret Key for Nessus')
    parser.add_argument('--conn_string', dest='conn_str',
            help='Connection string for Azure storage')
    parser.add_argument('--container', dest='container',
            help='Container for Azure blob storage')
    parser.add_argument('--folder', dest='folder', help='Folder for Azure file storage')
    parser.add_argument('--aws-url', dest='aws_url', help='URL to PUT files to in AWS')
    parser.add_argument('--api-key', dest='api_key', help='API key assigned for access')
    parser.add_argument('--repo', dest='repo', help='repo assigned')
    parser.add_argument('--version', action='version',
                    version='nessusScanUpload {version}'.format(version=__version__))
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    # Read command line arguments and config files
    import nessusScanUpload.logging_config
    from _version import __version__
    log = logging.getLogger('nessusScanUpload')
    
    cwd = os.path.dirname(__file__)

    args = parse_argv()

    config = load_config(args.configfile)

    try:
        if not args.access_key:
            args.access_key = config['nessus']['accessKey']
        if not args.secret_key:
            args.secret_key = config['nessus']['secretKey']
    except KeyError:
        highlight('Nessus Keys must be provided on command line or in Configuration file.')
        raise

    # Check for Azure configuration
    if not args.conn_str:
        args.conn_str = config['azure'].get('connection_string', None)
    if args.conn_str:
        if _no_azure_found:
            raise Exception('azure.storage.fileshare, azure.storage.blob or azure.core not installed.')
        _use_azure = True
        _method = 'azure'
    else:
        _use_azure = False

    if _use_azure:
        if not args.container:
            args.container = config['azure'].get('container', None)
        if not args.folder:
            args.folder = config['azure'].get('folder', None)

    if _use_azure and not (args.folder or args.container):
        highlight('Azure configuration must include either a blob storage'
                ' container or file folder.')
        raise Exception('Configuration Error.')
    # End Azure configuration

    # Check for AWS Configuration
    if not args.aws_url:
        args.aws_url = config['aws'].get('url', None)
    if args.aws_url:
        _use_aws = True
        _method = 'aws'
    else:
        _use_aws = False

    if _use_aws:
        if not args.api_key:
            args.api_key = config['aws'].get('api_key', None)
        if not args.repo:
            args.repo = config['aws'].get('repo', None)

    if _use_aws and not (args.api_key or args.repo):
        highlight('API key and repo id are required for sending files to AWS')
        raise Exception('Configuration Error.')


    args.nessus = config['nessus']
    args.aws = config['aws']

    if not args.savefile:
        args.savefile = config['savefile']['path']
    args.savefile = os.path.expanduser(args.savefile)

    savefile = configparser.ConfigParser()
    try:
        savefile.read_file(open(args.savefile))
    except FileNotFoundError:
        savefile['lastread'] = {}
    args.lastread = savefile['lastread']
   
    main(method=_method)
