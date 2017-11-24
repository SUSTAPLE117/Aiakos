import http.server
import ssl
import string
from secrets import choice


class AiakosServer(object):
    certificate_file = None

    def __init__(self, certificate_file):
        self.certificate_file = certificate_file

    def run(self):
        httpd = http.server.HTTPServer(('localhost', 443), http.server.SimpleHTTPRequestHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket, certfile=self.certificate_file, server_side=True)
        httpd.serve_forever()

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
