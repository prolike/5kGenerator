#!/bin/sh
docker run \
        -v $(pwd)/config.yml:/app/config.yml \
        prolike/5kgenerator:1.0.0