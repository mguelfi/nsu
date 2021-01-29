from nose.tools import assert_true
from unittest.mock import Mock, patch, ANY
from tempfile import NamedTemporaryFile
import requests
import logging
import sys

import nessusScanUpload.__main__
from _version import __version__
from scan_example import nessus

testargs = ["nessusScanUpload"]
#@patch('nessusScanUpload.__main__.logging.getLogger')
def test_parse_argv():
    nessusScanUpload.__main__.__version__ = __version__
    with patch.object(sys, 'argv', testargs):
        args = nessusScanUpload.__main__.parse_argv()
    assert(vars(args) == {'configfile': None, 'savefile': None,
        'access_key': None, 'secret_key': None, 'conn_str': None,
        'container': None, 'folder': None, 'aws_url': None,
        'api_key': None, 'repo': None})

def test_highlight():
    ret = nessusScanUpload.__main__.highlight('Test')
    assert(ret == None)

