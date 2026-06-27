#!/usr/bin/env bash
# wait-for-db.sh
# Can be used to pause execution until PostgreSQL is accepting connections.

set -e

host="$1"
shift
cmd="$@"

until pg_isready -h "$host" -U "${POSTGRES_USER:-jobpulse}"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
