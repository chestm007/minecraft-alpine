#! /bin/bash

docker run -ti --rm --name=minecraft \
           -e GCTHREADS=4 \
           -p 25565:25565 \
           -v /etc/localtime:/etc/localtime:ro \
           quay.io/chestm007/minecraft-alpine:$1
