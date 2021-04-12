#!/bin/bash

docker rm -f $(docker ps -a | grep -v "ci-server" | cut -d ' ' -f1)

docker ps -a
