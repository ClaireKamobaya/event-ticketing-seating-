USE `event_ticketing_seating`;

INSERT INTO `Attendee` (`registration_id`, `first_name`, `last_name`, `email`, `phone`)
VALUES 
('REG1001', 'Claire', 'Kamobaya', 'claire@example.com', '703-555-0101'),
('REG1002', 'James', 'Okafor', 'james@example.com', '703-555-0102'),
('REG1003', 'Amara', 'Diallo', 'amara@example.com', '703-555-0103');

INSERT INTO `Event` (`event_name`, `artist`, `event_date`, `venue`, `capacity`)
VALUES 
('AfroBeat Concert', 'Burna Boy', '2026-08-15', 'Jiffy Lube Live', 500),
('Reggae Night', 'Shatta Wale', '2026-09-10', 'The Anthem', 300),
('Jazz in the Park', 'Yemi Alade', '2026-10-05', 'Merriweather Post Pavilion', 800);

INSERT INTO `ticket_xref` (`attendee_id`, `event_id`, `ticket_id`, `confirmation_code`, `seat_number`, `purchase_date`)
VALUES 
(1, 1, 'TICK5001', 'CONF9001', 'A12', '2026-07-13'),
(2, 2, 'TICK5002', 'CONF9002', 'B05', '2026-07-14');