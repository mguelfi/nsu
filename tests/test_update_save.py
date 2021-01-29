from nose.tools import assert_true
from unittest.mock import Mock, patch, ANY
from tempfile import NamedTemporaryFile
import requests
import logging

import nessusScanUpload.__main__
from _version import __version__

#log = logging.getLogger()

@patch('nessusScanUpload.__main__.logging.getLogger')
def test_first_update_save(mock_logging):
    with NamedTemporaryFile() as tmp_save_file:
        scan_id = 999
        last_modification_date = 1608519152
        nessusScanUpload.__main__.update_save(scan_id, last_modification_date, tmp_save_file.name)
        tmp_save_file.seek(0)
        contents = tmp_save_file.read()
    mock_logging.assert_called_once()
    assert_true(contents == b'[lastread]\n999 = 1608519152\n\n')

@patch('nessusScanUpload.__main__.logging.getLogger')
def test_second_update_save(mock_logging):
    with NamedTemporaryFile() as tmp_save_file:
        scan_id = 999
        last_modification_date = 1608519152
        nessusScanUpload.__main__.update_save(scan_id, last_modification_date, tmp_save_file.name)
        scan_id = 994
        last_modification_date = 1608519148
        nessusScanUpload.__main__.update_save(scan_id, last_modification_date, tmp_save_file.name)
        tmp_save_file.seek(0)
        contents = tmp_save_file.read()
    assert mock_logging.call_count == 2
    assert_true(contents == b'[lastread]\n999 = 1608519152\n994 = 1608519148\n\n')

@patch('nessusScanUpload.__main__.logging.getLogger')
def test_overwrite_update_save(mock_logging):
    with NamedTemporaryFile() as tmp_save_file:
        scan_id = 999
        last_modification_date = 1608519152
        nessusScanUpload.__main__.update_save(scan_id, last_modification_date, tmp_save_file.name)
        scan_id = 994
        last_modification_date = 1608519148
        nessusScanUpload.__main__.update_save(scan_id, last_modification_date, tmp_save_file.name)
        scan_id = 999
        last_modification_date = 1608519168
        nessusScanUpload.__main__.update_save(scan_id, last_modification_date, tmp_save_file.name)
        tmp_save_file.seek(0)
        contents = tmp_save_file.read()
    assert mock_logging.call_count == 3
    assert_true(contents == b'[lastread]\n999 = 1608519168\n994 = 1608519148\n\n')

