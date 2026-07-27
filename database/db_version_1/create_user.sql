CREATE USER IF NOT EXISTS 'event_ticketing_user'@'localhost' IDENTIFIED BY '';

GRANT ALL PRIVILEGES ON `event_ticketing_seating`.* TO 'event_ticketing_user'@'localhost';

FLUSH PRIVILEGES;