import telnetlib
import json

with open("devices.json", "r") as devices_list:
    devices = json.loads(devices_list.read())

for ip in devices.keys():
    print("Flashing: {} ".format(ip))

    users = devices[ip]
    for username in users.keys():
        password = users[username]
        tn = telnetlib.Telnet(ip)

        tn.read_until(b"Login: ")
        tn.write(username.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

        tn.write(b"sh\n")
        tn.write(b"exit\n")
        tn.write(b"exit\n")

        print(tn.read_all().decode('ascii'))
