#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#


"""This can also be used with keyring command line tool

    python -m keyring -b clach04.keyring.SimpleKeyring get testsvc testuser
    python -m keyring -b clach04.keyring.DumbServer get testsvc testuser
"""

import logging
try:
    # Py3
    from urllib.error import HTTPError
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode
except ImportError:
    # Py2
    from urllib2 import urlopen, Request, HTTPError
    from urllib import urlencode


import keyring  # python -m pip install keyring
import keyring.backend


log = logging.getLogger(__name__)
logging.basicConfig()
#logging.basicConfig(level=logging.DEBUG)
#log.setLevel(level=logging.DEBUG)


def urllib_get_url(url, headers=None, ignore_errors=False):
    """
    @url - web address/url (string)
    @headers - dictionary - optional
    """
    log.debug('get_url=%r', url)
    #log.debug('headers=%r', headers)
    response = None
    try:
        if headers:
            request = Request(url, headers=headers)
        else:
            request = Request(url)  # may not be needed
        response = urlopen(request)
        url = response.geturl()  # may have changed in case of redirect
        code = response.getcode()
        #log("getURL [{}] response code:{}".format(url, code))
        result = response.read()
        return result
    except:  # HTTPError, ConnectionRefusedError
        # probably got HTTPError, may be ConnectionRefusedError
        if ignore_errors:
           return None
        else:
           raise
    finally:
        if response != None:
            response.close()


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


DEFAULT_SERVER_PORT = 4277  # FIXME pull in from dumbserver

class DumbServer(keyring.backend.KeyringBackend):
    """http server access, local only across regular tcp_ip socket (no need for unix domain sockets)
    ONLY uses GET calls (not POST)
    """
    def __init__(self):
        self._server_url = 'http://127.0.0.1:%d/' % DEFAULT_SERVER_PORT

    priority = 0  # if this is one, then the chainer backend may pick this over (say) WinVaultKeyring (even though that's a 5)

    def supported(self):
        return 0

    def get_password(self, service, username):
        log.debug('get_password called')
        vars = {
            'service': service,
            'username': username,
        }
        url = self._server_url + 'get' + '?' + urlencode(vars)
        log.debug('get_password url=%r', url)
        password = urllib_get_url(url, ignore_errors=True)
        if password is not None:
            password = password.decode('utf-8')
        return password

    def set_password(self, service, username, password):
        # NOOP - could do the same as get_password
        return 0  # return something else?

    def delete_password(self, service, username):
        # NOOP
        pass
