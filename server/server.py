import csv
import http.server
import json
import logging
import ssl
import string
from secrets import choice
from urllib.parse import parse_qs, urlparse


class AiakosServer(http.server.SimpleHTTPRequestHandler):
    def _set_response(self, password_length):

        self.send_response(200)
        self.send_header('Content-Type', 'text/json')
        self.send_header('Content-Length', password_length + 2)
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

    @staticmethod
    def write_password_to_file(client_ip, username, password, ):
        with open('passwords.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([client_ip, username, password])

    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        password_length = int(query_components["password_length"][0])
        username = str(query_components["username"][0])
        self._set_response(password_length)
        new_password = self.generate_password(password_length)
        self.write_password_to_file(username=username, password=new_password, client_ip=self.client_address[0])
        response_data = json.dumps(new_password)
        self.wfile.write(response_data.encode('utf-8'))


def run(handler_class=AiakosServer, certificate_file=None, key_file=None):
    logging.basicConfig(level=logging.INFO)

    httpd = http.server.HTTPServer(('0.0.0.0', 8080), handler_class)
    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=key_file, certfile=certificate_file, server_side=True)

    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == "__main__":
    run(certificate_file="certificate.pem", key_file="key.pem")
