#!/bin/bash

TAG=`curl https://pypi.python.org/pypi/dserve/json | jq -r .info.version`

# Build docker image
docker build --no-cache  -t jicscicomp/dserve:$TAG deploy/docker/
docker tag jicscicomp/dserve:$TAG jicscicomp/dserve:latest
