#!/usr/bin/env python3
import os
import logging
import logging.handlers
import platform

"""
All the logging configuration

NB: looks in the shell environment for DEBUG, in a bash shell:
    # export DEBUG=true
    to enable logging to console
    # export -n DEBUG
    to turn it off
"""

log = logging.getLogger()
log.setLevel(logging.INFO)

formatter = logging.Formatter('%(name)s %(module)s %(levelname)s: %(message)s')


if platform.system() == "Linux":
    handler = logging.handlers.SysLogHandler(address = '/dev/log')
elif platform.system() == "Windows" or platform.python_implementation() == "IronPython":
    hander = logging.handlers.NTEventLogHandler(__name__)

handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

log.addHandler(handler)

if os.environ.get('DEBUG'):
    print('DEBUG enabled')
    log.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    log.addHandler(console)

# Quiet library loggers down...
azure_logger = logging.getLogger('azure.core.pipeline.policies.http_logging_policy')
azure_logger.setLevel(logging.WARN)
urllib3_logger = logging.getLogger('urllib3.connectionpool')
urllib3_logger.setLevel(logging.WARN)
tenable_logger = logging.getLogger('tenable.nessus.Nessus')
tenable_logger.setLevel(logging.WARN)

