#!/bin/ash

adduser admin -S -s /bin/ash

passwd admin < new_pass

./busybox telnetd -l /bin/login

/bin/ash
