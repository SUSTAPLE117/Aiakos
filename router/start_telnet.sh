#!/bin/ash

passwd < new_pass

cat new_securetty >> /etc/securetty

./busybox telnetd -l /bin/login

/bin/ash
