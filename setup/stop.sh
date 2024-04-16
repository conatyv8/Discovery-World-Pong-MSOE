#!/bin/bash

compose='docker compose' #'podman-compose'

./close_windows.sh

docker compose down
