#!/bin/sh


IMAG_NAME=$(cat ../.env | grep TAG | cut -d'=' -f2)
CONTAINER_NAME=$(docker ps | grep $IMAG_NAME | awk '{print $NF}')
PORT=$(docker inspect $CONTAINER_NAME | grep HostPort | awk -F':' '{print $2}' | cut -d'"' -f2 | uniq)
ADDRESS=$(docker inspect $CONTAINER_NAME | grep -a4 NetworkID | grep IPAddress | awk -F':' '{print $2}' | cut -d'"' -f2 | uniq | grep -v null)
APIS="index batch-weight unknown item session post weight"



for url in $APIS
do
    wget "http://$ADDRESS:$PORT/$url"
done

