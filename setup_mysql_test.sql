-- this sql script creates a database, then creates a user of that database
-- It then sets up the credentials of the user with username and password.
-- The script also grants priviledges to the uses.

-- Create the hbnb_test_db database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create the hbnb_test user if it doesn't exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on hbnb_test_db to hbnb_test
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on performance_schema to hbnb_test
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;

