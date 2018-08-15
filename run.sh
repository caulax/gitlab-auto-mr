#!/usr/bin/env bash

# docker build -t glmr .
docker run -v `pwd`/.settings.yaml:/var/app/.settings.yaml --rm glmr
