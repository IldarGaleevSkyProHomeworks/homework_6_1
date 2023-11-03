import os
import sys
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from os import path
import logging

WWW_ROOT_PATH = path.join(os.getcwd(), 'www_root')

logger = logging.getLogger('http_server')


class LoggedSimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        super().do_GET()
        logger.info(f'GET: {self.path}')

    def do_POST(self):
        self.send_error(405, 'Not implemented yet.')
        logger.info(f'POST: {self.path}')


if __name__ == '__main__':

    try:
        logger.setLevel(logging.INFO)
        log_handler = logging.StreamHandler(sys.stdout)
        log_handler.setLevel(logging.INFO)
        logger.addHandler(log_handler)

        handler = partial(LoggedSimpleHTTPRequestHandler, directory=WWW_ROOT_PATH)

        httpd = HTTPServer(('localhost', 8080), handler)
        host, port = httpd.socket.getsockname()[:2]
        url_host = f'[{host}]' if ':' in host else host
        print(
            f"Serving HTTP on {host} port {port} "
            f"(http://{url_host}:{port}/) ..."
        )

        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped")
    except Exception as e:
        logger.error(e)
