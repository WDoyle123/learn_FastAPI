#!/bin/bash

set -e

source ../.env

export PGPASSWORD="$DATABASE_PASSWORD"

psql -U "$DATABASE_USERNAME" -d "$DATABASE_NAME" -h "$DATABASE_HOST" -p "$DATABASE_PORT" -c "DROP TABLE users CASCADE;"


