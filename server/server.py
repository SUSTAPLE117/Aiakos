import http.server
import ssl

httpd = http.server.HTTPServer(('localhost', 443), http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile='', server_side=True)
httpd.serve_forever()
