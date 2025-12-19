#!/bin/sh
set -e

echo "Starting entrypoint: attempting to initialize database (if reachable)"

# Retry initialization several times to wait for DB readiness in compose setups
MAX_TRIES=12
DELAY=2
TRY=1
while [ $TRY -le $MAX_TRIES ]; do
  echo "Init attempt $TRY/$MAX_TRIES..."
  if python -m app.scripts.init_db; then
    echo "DB init succeeded"
    break
  else
    echo "DB init failed — sleeping ${DELAY}s and retrying"
    TRY=$((TRY+1))
    sleep $DELAY
  fi
done

echo "Starting Uvicorn"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
