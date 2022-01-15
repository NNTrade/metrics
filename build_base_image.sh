#!bin/bash
docker build -t trading-metrics/base-img --ssh default --no-cache -f ./.devcontainer/base/Dockerfile .