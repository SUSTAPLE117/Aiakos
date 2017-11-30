FROM alpine:latest

WORKDIR /root/

RUN apk add --update openssl

RUN wget "https://busybox.net/downloads/binaries/1.26.2-defconfig-multiarch/busybox-x86_64" -O busybox

RUN chmod +x busybox

ADD start_telnet.sh .

ADD new_securetty .

ADD new_pass .

RUN chmod +x start_telnet.sh

CMD /root/start_telnet.sh

EXPOSE 23
