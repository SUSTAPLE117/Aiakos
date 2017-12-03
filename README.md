# Aiakos

## Create certificate and keyfile

`openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem`

## Build router Docker image

`docker build . -t aiakos-router`

## Start router
`docker run -dit --net=host aiakos-router`