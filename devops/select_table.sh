source ../.env

echo $DB_USER

psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -c "SELECT * FROM users;"

