from __future__ import absolute_import

import argparse
import os
import subprocess
import sys
import threading
import time

import SimpleHTTPServer
import SocketServer


class Server(SocketServer.TCPServer):
    allow_reuse_address = True


def handler_bind(directory):
    class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')

            SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

        def translate_path(self, path):
            while path.startswith('/'):
                path = path[1:]

            path = os.path.join(directory, path)
            return SimpleHTTPServer.SimpleHTTPRequestHandler.translate_path(self, path)

        def log_message(self, format, *args):
            pass

    return Handler


class SocketThread(threading.Thread):
    def __init__(self, directory, host):
        threading.Thread.__init__(self)

        if not ':' in host:
            self.host = host
            self.port = 6060
        else:
            self.host, port = host.split(':')
            self.port = int(port)

        self.httpd = Server((self.host, self.port), handler_bind(directory))

    def shutdown(self):
        self.httpd.shutdown()
        self.httpd.server_close()

    def run(self):
        self.httpd.serve_forever()


def run(args):
    parser = argparse.ArgumentParser(description='clang based documentation generator.',
                                     usage='%(prog)s serve [OPTIONS] [DIRECTORY]')

    parser.add_argument('--address', default=':6060', metavar='HOST:PORT',
                        help='address (host:port) on which to serve documentation')

    parser.add_argument('directory', nargs='?', help='directory to serve', default='.')

    opts = parser.parse_args(args)

    t = SocketThread(opts.directory, opts.address)
    t.start()

    dn = open(os.devnull, 'w')

    if t.host == '':
        url = 'http://localhost:{0}/'.format(t.port)
    else:
        url = 'http://{0}:{1}/'.format(t.host, t.port)

    if sys.platform.startswith('darwin'):
        subprocess.call(('open', url), stdout=dn, stderr=dn)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', url), stdout=dn, stderr=dn)

    while True:
        try:
            time.sleep(3600)
        except KeyboardInterrupt:
            t.shutdown()
            t.join()
            break
