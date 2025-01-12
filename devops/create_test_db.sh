#!/bin/bash

export $(grep -v '^#' ../.env | xargs)

DATABASE_USERNAME=${DATABASE_USERNAME}_test
DATABASE_NAME=${DATABASE_NAME}_test
DATABASE_HOSTNAME=${DATABASE_HOSTNAME}
DATABASE_PORT=${DATABASE_PORT}
DATABASE_PASSWORD=${DATABASE_PASSWORD}

export PGPASSWORD="$DATABASE_PASSWORD"

psql -h "$DATABASE_HOSTNAME" -U postgres -p "$DATABASE_PORT" -c "DO
\$do\$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = '$DATABASE_USERNAME'
   ) THEN
      CREATE ROLE $DATABASE_USERNAME LOGIN PASSWORD '$DATABASE_PASSWORD';
   END IF;
END
\$do\$;"

if [ $? -ne 0 ]; then
    echo "Error creating user '$DATABASE_USERNAME'."
    exit 1
fi

psql -h "$DATABASE_HOSTNAME" -U postgres -p "$DATABASE_PORT" -c "CREATE DATABASE $DATABASE_NAME OWNER $DATABASE_USERNAME;" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "Database '$DATABASE_NAME' created successfully."
else
    echo "Database '$DATABASE_NAME' already exists or an error occurred."
fi

