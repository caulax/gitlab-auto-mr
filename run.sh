#!/usr/bin/env bash

docker build -t glmr .
docker run --rm glmr python main.py -a accept-mr -f projects-list.yaml
