#!/bin/sh


IMAG_NAME=$(cat ../.env | grep TAG | cut -d'=' -f2)
CONTAINER_NAME=$(docker ps | grep $IMAG_NAME | awk '{print $NF}')
PORT=$(docker inspect $CONTAINER_NAME | grep HostPort | awk -F':' '{print $2}' | cut -d'"' -f2 | uniq)
ADDRESS=$(docker inspect $CONTAINER_NAME | grep -a4 NetworkID | grep IPAddress | awk -F':' '{print $2}' | cut -d'"' -f2 | uniq | grep -v null)
APIS="index weight session item batch-weight unknown"

for url in $APIS
do
    wget "http://18.194.15.175:8085/$url"
done



