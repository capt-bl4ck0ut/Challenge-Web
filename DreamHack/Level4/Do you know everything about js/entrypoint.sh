#!/bin/sh
set -eu
( cd "/app/backend" && node "dist/main.js" ) &
BACK_PID=$!
node "/app/frontend/.output/server/index.mjs" &
FE_PID=$!
trap "kill -TERM \"$BACK_PID\" \"$FE_PID\" 2>/dev/null || true" INT TERM
while :; do
  kill -0 "$BACK_PID" 2>/dev/null || exit 1
  kill -0 "$FE_PID" 2>/dev/null || exit 1
  sleep 1
done
