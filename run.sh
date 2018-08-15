#!/usr/bin/env bash

# docker build -t glmr .
docker run -v `pwd`/.settings.yaml --rm glmr
