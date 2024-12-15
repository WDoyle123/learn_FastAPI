#!/bin/bash

set -e

source ../.secrets.sh

SQL_COMMANDS="
DO \$\$
BEGIN
    -- Step 1: Create User if not exists
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles WHERE rolname = '${DB_USER}'
    ) THEN
        CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';
        RAISE NOTICE 'User ${DB_USER} created.';
    ELSE
        RAISE NOTICE 'User ${DB_USER} already exists.';
    END IF;

    -- Step 2: Allow the new user to log in
    ALTER ROLE ${DB_USER} LOGIN;

    -- Step 3: Create Database if not exists
    IF NOT EXISTS (
        SELECT FROM pg_database WHERE datname = '${DB_NAME}'
    ) THEN
        CREATE DATABASE ${DB_NAME};
        RAISE NOTICE 'Database ${DB_NAME} created.';
    ELSE
        RAISE NOTICE 'Database ${DB_NAME} already exists.';
    END IF;

    -- Step 4: Assign the database owner
    ALTER DATABASE ${DB_NAME} OWNER TO ${DB_USER};
    RAISE NOTICE 'Database ${DB_NAME} ownership assigned to ${DB_USER}.';
END \$\$;
"

# Execute the commands
psql "$DB_SUPERUSER" -h "$DB_HOST" -p "$DB_PORT" -c "$SQL_COMMANDS"

echo "User and database setup completed."

