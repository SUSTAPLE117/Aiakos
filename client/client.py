import telnetlib
import json
import requests


class Aiakos(object):
    def __init__(self):
        self.devices = None
        self.users = None
        self.tn = None
        self.config = None

    def read(self):
        data = ""
        while True:
            response = self.tn.read_until(b"\n", timeout=2)
            response = response.decode("ascii")
            if response == "":
                return data
            data += response


    def send_telnet_command(self, command):
        self.tn.write(command)
        return self.read()


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
                result = self.tn.read_until(b"\n")

    def change_password(self, new_password):

        self.tn.write(b"passwd\n")
        self.tn.read_until(b"New password:")
        self.tn.write(new_password.encode("ascii") + b"\n")
        self.tn.read_until(b"Retype password:")
        self.tn.write(new_password.encode("ascii") + b"\n")
        print(self.tn.read_all())

    def exit_telnet(self):
        self.tn.write(b"exit\n")

    def install_ssh(self):
        # openrc package needed to start sshd
        response = self.send_telnet_command(b"apk add openrc\n")
        # package containing sshd
        response = self.send_telnet_command(b"apk add openssh\n")

        response = self.send_telnet_command(b"wget http://svieg.com/sshd_config\n")
        # custom config to allow root logins with password
        response = self.send_telnet_command(b"mv sshd_config /etc/ssh/sshd_config\n")
        # Adding sshd at boot
        response = self.send_telnet_command(b"rc-update add sshd\n")
        # starting sshd
        response = self.send_telnet_command(b"rc-status\n")
        response = self.send_telnet_command(b"touch /run/openrc/softlevel\n")
        response = self.send_telnet_command(b"/etc/init.d/sshd start\n")
        return

    def request_new_password(self):
        url = "{}/password_length?={}".format(self.config["server_url"],
                                              self.config["password_length"])
        command = "wget -qO- {} --no-check-certificate\n".format(url)
        self.tn.write(command.encode("ascii"))
        response = self.tn.read_all()
        return "password"

    def flash_device(self, device):

        self.connect_telnet(device)
        self.install_ssh()
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
