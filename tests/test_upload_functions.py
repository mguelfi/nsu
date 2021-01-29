from nose.tools import assert_true
from unittest.mock import Mock, patch, ANY
from tempfile import TemporaryFile
import requests
import sys

import nessusScanUpload.__main__
from _version import __version__

testargs = ["nessusScanUpload"]

@patch('nessusScanUpload.__main__.requests.put')
def test_put_upload(mock_put):
    # Mock the requests.put() call
    mock_put.return_value.ok = True
    # Setup nessusScanUpload.__main__.args
    nessusScanUpload.__main__.__version__ = __version__
    with patch.object(sys, 'argv', testargs):
        nessusScanUpload.__main__.args = nessusScanUpload.__main__.parse_argv()

    # Set args we want to check
    aws = {}
    aws['ssl_verify'] = 'true'
    nessusScanUpload.__main__.args.aws = aws
    nessusScanUpload.__main__.args.aws_url = \
       'https://b0cfrixog2.execute-api.ap-southeast-2.amazonaws.com/prod'
    nessusScanUpload.__main__.args.repo = '999'

    expected = {'configfile': None, 'savefile': None, 'access_key': None,
            'secret_key': None, 'conn_str': None, 'container': None, 'folder': None,
            'aws_url': 'https://b0cfrixog2.execute-api.ap-southeast-2.amazonaws.com/prod',
            'api_key': None, 'repo': '999', 'aws': {'ssl_verify': 'true'}}

    with TemporaryFile() as fp:
        nessusScanUpload.__main__.put_upload(fp, 'test_scan')

    # Confirm that the request-response cycle completed successfully.
    assert_true(vars(nessusScanUpload.__main__.args) == expected)
    mock_put.assert_called_with(
            'https://b0cfrixog2.execute-api.ap-southeast-2.amazonaws.com/prod/999/test_scan',
            data=ANY,
            headers={'x-api-key': None,
                'content-encoding': 'gzip'},
            verify=True)


@patch('nessusScanUpload.__main__.ShareFileClient')
def test_file_upload(mock_sfc):
    # mocking ShareFileClient means we are only testing the function hasn't changed..
    mock_sfc.return_value.ok = True
    nessusScanUpload.__main__.__version__ = __version__
    with patch.object(sys, 'argv', testargs):
        nessusScanUpload.__main__.args = nessusScanUpload.__main__.parse_argv()

    with TemporaryFile() as fp:
        nessusScanUpload.__main__.file_upload(fp, 'test_scan')

@patch('nessusScanUpload.__main__.BlobServiceClient')
def test_blob_upload(mock_bsc):
    # mocking BlobServiceClient means we are only testing the function hasn't changed..
    mock_bsc.return_value.ok = True
    nessusScanUpload.__main__.__version__ = __version__
    with patch.object(sys, 'argv', testargs):
        nessusScanUpload.__main__.args = nessusScanUpload.__main__.parse_argv()

    with TemporaryFile() as fp:
        nessusScanUpload.__main__.blob_upload(fp, 'test_scan')


