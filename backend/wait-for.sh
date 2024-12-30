#!/bin/sh
set -e

host="$1"
shift

until python -c "import socket; socket.create_connection((\"$host\", 5432))"; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

exec "$@"
