USE `event_ticketing_seating`;

INSERT INTO `Attendee` (`registration_id`, `first_name`, `last_name`, `email`, `phone`)
VALUES ('REG1001', 'Claire', 'Kamobaya', 'claire@example.com', '703-555-0101');

INSERT INTO `Event` (`event_name`, `artist`, `event_date`, `venue`, `capacity`)
VALUES ('AfroBeat Concert', 'Burna Boy', '2026-08-15', 'Jiffy Lube Live', 500);

INSERT INTO `ticket_xref` (`attendee_id`, `event_id`, `ticket_id`, `confirmation_code`, `seat_number`, `purchase_date`)
VALUES (1, 1, 'TICK5001', 'CONF9001', 'A12', '2026-07-13');