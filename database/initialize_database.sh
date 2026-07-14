#!/bin/bash

MYSQL="/c/MAMP/bin/mysql/bin/mysql.exe"
USER="root"
PASS="root"
HOST="localhost"
PORT="3306"

echo "Dropping database..."
"$MYSQL" -u "$USER" -h "$HOST" -P "$PORT" -p"$PASS" < database/drop_database.sql

echo "Creating database..."
"$MYSQL" -u "$USER" -h "$HOST" -P "$PORT" -p"$PASS" < database/create_database.sql

echo "Dropping user..."
"$MYSQL" -u "$USER" -h "$HOST" -P "$PORT" -p"$PASS" < database/drop_user.sql

echo "Creating user..."
"$MYSQL" -u "$USER" -h "$HOST" -P "$PORT" -p"$PASS" < database/create_user.sql

echo "Creating tables..."
"$MYSQL" -u "$USER" -h "$HOST" -P "$PORT" -p"$PASS" < database/create_tables.sql

echo "Loading test data..."
"$MYSQL" -u "$USER" -h "$HOST" -P "$PORT" -p"$PASS" < database/initialize_test_data.sql

echo "Done!"