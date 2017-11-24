import telnetlib
import json


class Aiakos(object):
    def __init__(self):
        self.devices = None
        self.users = None
        self.tn = None

    def get_devices(self, filename):

        with open(filename, "r") as devices_list:
            self.devices = json.loads(devices_list.read())

    def connect_telnet(self, username):
        password = self.users[username]
        self.tn = telnetlib.Telnet(ip)

        self.tn.read_until(b"Login: ")
        self.tn.write(username.encode('ascii') + b"\n")
        self.tn.read_until(b"Password: ")
        self.tn.write(password.encode('ascii') + b"\n")

    def change_password(self, new_password):

        self.tn.write(b"passwd\n")
        self.tn.read_until(b"New password:")
        self.tn.write(new_password.encode("ascii") + b"\n")
        self.tn.write(b"exit\n")

    def request_new_password(self):

        # FIXME: request password to server.
        return "password"

    def flash_device(self, ip):

        print("Flashing: {} ".format(ip))

        self.users = self.devices[ip]
        for username in self.users.keys():
            self.connect_telnet(username)
            new_password = self.request_new_password()
            self.change_password(new_password)
            print(self.tn.read_all().decode('ascii'))

    def run(self):

        self.get_devices("devices.json")

        for ip in self.devices.keys():
            self.flash_device(ip)


if __name__ == "__main__":
    aiakos = Aiakos()
    aiakos.run()
