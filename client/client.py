import telnetlib
import json
import secrets
import string

class Aiakos(object):

    def __init__(self):
        self.devices = None
        self.users = None
        self.tn = None

    def get_devices(self, filename):

        with open(filename, "r") as devices_list:
            self.devices = json.loads(devices_list.read())

    def connect_telnet(self, user):
        password = self.users[username]
        self.tn = telnetlib.Telnet(ip)

        self.tn.read_until(b"Login: ")
        self.tn.write(username.encode('ascii') + b"\n")
        self.tn.read_until(b"Password: ")
        self.tn.write(password.encode('ascii') + b"\n")

    def generate_password(self):
        
        alphabet = string.ascii_letters + string.digits
        while True:
            password = ''.join(choice(alphabet) for i in range(10)) # TODO: custom length
            if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3): # TODO: custom number length
        break
        return password

    def change_password(self, new_password):

        self.tn.write(b"passwd\n")
        self.tn.read_until(b"New password:")
        self.tn.write(new_password.encode("ascii") + b"\n")
        self.tn.write(b"exit\n")

    def flash_device(self, ip):

        print("Flashing: {} ".format(ip))

        self.users = self.devices[ip]
        for username in users.keys():
            connect_telnet(username)
            new_password = generate_password()
            change_password(new_password)
            print(self.tn.read_all().decode('ascii'))

    def run():

        get_devices("devices.json")

        for ip in devices.keys():
            flash_device(ip)


for ip in devices.keys():
if __name__ == "__main__":
    aiakos = Aiakos()
    aiakos.run()
