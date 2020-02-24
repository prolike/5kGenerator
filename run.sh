#!/bin/sh
docker run \
        -v $(pwd)/config.yml:/app/config.yml \
        5kgenerator:local-build