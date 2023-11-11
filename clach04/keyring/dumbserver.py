#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""web server

Uses WSGI, see http://docs.python.org/library/wsgiref.html

Python 2 or Python 3


    python -m clach04.keyring.dumbserver

"""


try:
    # py3
    from urllib.parse import parse_qs
except ImportError:
    # py2 (and <py3.8)
    from cgi import parse_qs
try:
    import getpass
except ImportError:
    # Mayhe Jython... old version
    class getpass(object):
        def getpass(cls, prompt=None, stream=None):
            if prompt is None:
                prompt = ''
            if stream is None:
                stream = sys.stdout
            prompt = prompt+ ' (warning password WILL echo): '
            stream.write(prompt)
            result = raw_input('') # or simply ignore stream??
            return result
        getpass = classmethod(getpass)

import os
import logging
import mimetypes
import sys
import time
from wsgiref.simple_server import make_server

try:
    import bjoern
except ImportError:
    bjoern = None

try:
    import cheroot  # CherryPy Server https://cheroot.cherrypy.dev/en/latest/pkg/cheroot.wsgi/
except ImportError:
    cheroot = None

try:
    import meinheld  # https://github.com/mopemope/meinheld
except ImportError:
    meinheld = None


DEFAULT_SERVER_PORT = 4277

log = logging.getLogger(__name__)
logging.basicConfig()
log.setLevel(level=logging.DEBUG)


MODE_STATIC = 'static'  # uses global single_password
MODE_PROMPT = 'prompt'  # uses global single_password, but prompt at start up time
run_mode = MODE_STATIC
single_password = 'password'

def simple_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    result= []

    path_info = environ['PATH_INFO']

    # Returns a dictionary in which the values are lists
    if environ.get('QUERY_STRING'):
        get_dict = parse_qs(environ['QUERY_STRING'])
    else:
        get_dict = {}  # wonder if should make None to make clear its not there at all
    log.debug('path_info %r', path_info)
    log.debug('get_dict %r', get_dict)

    if path_info == '/get':
        # can either proxy get_dict into a different keyring backend...
        # or hard code to support only a single password
        if run_mode == MODE_STATIC:
            result.append(single_password.encode('utf-8'))
        else:
            raise NotImplementedError('run_mode-%r' % run_mode)

    start_response(status, headers)
    return result


def main(argv=None):
    if argv is None:
        argv = sys.argv

    print('Python %s on %s' % (sys.version, sys.platform))

    global run_mode
    try:
        run_mode = argv[1]
    except IndexError:
        # default
        run_mode = MODE_STATIC
    if run_mode == MODE_PROMPT:
        run_mode = MODE_STATIC
        global single_password
        single_password = getpass.getpass("Password:")

    server_port = int(os.environ.get('DUMB_SERVER_KEYRING_PORT', os.environ.get('PORT', DEFAULT_SERVER_PORT)))
    server_listen_address = '127.0.0.1'  # ::1 - do not want to listen on 0.0.0.0

    log.info('Starting server: %r', (server_listen_address, server_port))
    log.info('Starting server: http://%s:%d', server_listen_address, server_port)
    log.info('Issue CTRL-C (CTRL-Break Windows) to stop')
    if bjoern:
        # Untested
        log.info('Using: bjoern')
        bjoern.run(simple_app, server_listen_address, server_port)
    elif cheroot:
        # Untested
        log.info('Using: cheroot (from CherryPy)')
        server = cheroot.wsgi.Server((server_listen_address, server_port), my_crazy_app)
        server.start()
    elif meinheld:
        # Untested
        log.info('Using: meinheld')
        meinheld.server.listen((server_listen_address, server_port))  # does not accept ''
        meinheld.server.run(simple_app)
    else:
        log.info('Using: wsgiref.simple_server')
        httpd = make_server(server_listen_address, server_port, simple_app)
        httpd.serve_forever()

if __name__ == "__main__":
    sys.exit(main())
