import telnetlib
import json
import requests


class Aiakos(object):
    def __init__(self):
        self.devices = None
        self.users = None
        self.tn = None
        self.config = None

    def load_config(self):
        with open("config.json", "r") as config_file:
            self.config = json.loads(config_file.read())

    def get_devices(self, filename):

        with open(filename, "r") as devices_list:
            self.devices = json.loads(devices_list.read())

    def connect_telnet(self, device):
        for ip in device.keys():
            users = device[ip]
            for username in users.keys():
                self.tn = telnetlib.Telnet(ip)
                self.tn.read_until(b"login: ")
                self.tn.write(username.encode('ascii') + b"\n")
                self.tn.read_until(b"Password: ")
                password = users[username]
                self.tn.write(password.encode('ascii') + b"\n")

    def change_password(self, new_password):

        self.tn.write(b"passwd\n")
        self.tn.read_until(b"New password:")
        self.tn.write(new_password.encode("ascii") + b"\n")
        self.tn.read_until(b"Retype password:")
        self.tn.write(new_password.encode("ascii") + b"\n")
        self.tn.write(b"exit\n")

    def request_new_password(self):
        payload = {"password_length" : self.config["password_length"]}
        response = requests.get(self.config["server_url"], params=payload,verify=False)
        return "password"

    def flash_device(self, device):

        self.connect_telnet(device)
        new_password = self.request_new_password()
        self.change_password(new_password)
        print(self.tn.read_all().decode('ascii'))

    def run(self):
        self.load_config()
        self.get_devices("devices.json")

        for device in self.devices:
            self.flash_device(device)


if __name__ == "__main__":
    aiakos = Aiakos()
    aiakos.run()
