#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#


"""This can also be used with keyring command line tool

    python -m keyring -b clach04.keyring.SimpleKeyring get testsvc testuser
"""

import logging

import keyring  # python -m pip install keyring
import keyring.backend


log = logging.getLogger(__name__)
logging.basicConfig()
#logging.basicConfig(level=logging.DEBUG)
#log.setLevel(level=logging.DEBUG)


class SimpleKeyring(keyring.backend.KeyringBackend):
    """Simple Keyring is a keyring which can store only one
    password in memory.
    """
    def __init__(self):
        self.password = ''

    priority = 1

    def supported(self):
        return 0

    def get_password(self, service, username):
        log.debug('get_password called')
        return self.password

    def set_password(self, service, username, password):
        self.password = password
        return 0

    def delete_password(self, service, username):
        self.password = None
