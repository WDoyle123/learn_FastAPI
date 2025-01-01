#!/bin/bash

set -e

source ../.secrets.sh

export PGPASSWORD="$DB_PASSWORD"

psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -c "DROP TABLE users;"

