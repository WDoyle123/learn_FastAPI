#!/bin/bash

set -e

source ../.secrets.sh

export PGPASSWORD="$DB_PASSWORD"

psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -c "
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content VARCHAR(255) NOT NULL,
    published BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
"

echo "Table 'posts' created successfully."

psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -c "DELETE FROM posts;"
psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -c "ALTER SEQUENCE posts_id_seq RESTART WITH 1;"

echo "Table 'posts' cleared and sequence reset."

psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -c "
INSERT INTO posts (title, content, published) VALUES
('title0', 'this is content 0', FALSE),
('title1', 'this is content 1', TRUE),
('title2', 'this is content 2', FALSE),
('title3', 'this is content 3', FALSE),
('title4', 'this is content 4', FALSE),
('title5', 'this is content 5', TRUE),
('title6', 'this is content 6', TRUE),
('title7', 'this is content 7', FALSE),
('title8', 'this is content 8', FALSE),
('title9', 'this is content 9', TRUE);
"

echo "Mock data inserted into 'posts' table successfully."

