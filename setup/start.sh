#!/bin/bash

compose='docker compose' #'podman-compose'

$compose up -d

./open_windows.sh
