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
@patch('nessusScanUpload.__main__.logging.getLogger')
def test_find_scans(mock_logging):
    nessusScanUpload.__main__.__version__ = __version__
    with patch.object(sys, 'argv', testargs):
        nessusScanUpload.__main__.args = nessusScanUpload.__main__.parse_argv()
    nessusScanUpload.__main__.args.lastread = False
    scans, lastread = nessusScanUpload.__main__.find_scans(nessus)
    assert(scans[12] == [204])
    assert(scans[8] == [203])
    assert(lastread == {12: 1611194784, 8: 1611105887})
    mock_logging.assert_called_once()

