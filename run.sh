#!/usr/bin/env bash

docker build -t glmr .
docker run --rm glmr python main.py -a create-mr -f projects-list.yaml
