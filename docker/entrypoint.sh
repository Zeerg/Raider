#!/bin/bash

# source env
set -a 
echo "Sourcing /app/.env"
source /app/.env

# start tor
echo "Starting Tor"
/usr/sbin/tor &

# run
exec "$@"