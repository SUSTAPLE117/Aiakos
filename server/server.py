import http.server
import json
import logging
import ssl
import string
from secrets import choice
from urllib.parse import parse_qs, urlparse


class AiakosServer(http.server.SimpleHTTPRequestHandler):
    def _set_response(self):

        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    @staticmethod
    def generate_password(password_length):

        alphabet = string.ascii_letters + string.digits
        while True:
            password = ''.join(choice(alphabet) for i in range(password_length))
            if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.lower() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
                break
        return password

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        query_components = parse_qs(urlparse(self.path).query)
        password_length = query_components["password_length"]
        self._set_response()
        response_data = json.dumps(self.generate_password(password_length))
        self.wfile.write(response_data)


def run(handler_class=AiakosServer, certificate_file=None, key_file=None):
    logging.basicConfig(level=logging.INFO)

    httpd = http.server.HTTPServer(('localhost', 8080), handler_class)
    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=key_file, certfile=certificate_file, server_side=True)

    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == "__main__":
    run(certificate_file="certificate.pem",key_file="key.pem")
