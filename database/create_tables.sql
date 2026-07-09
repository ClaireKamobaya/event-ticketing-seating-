SET FOREIGN_KEY_CHECKS=0;

USE `event_ticketing_seating`;

-- ---------------------------------
-- ATTENDEE TABLE
DROP TABLE IF EXISTS `Attendee`;

CREATE TABLE IF NOT EXISTS `Attendee` (
    `id` int(11) NOT NULL,
    `registration_id` varchar(20) NOT NULL,
    `first_name` varchar(25) NOT NULL,
    `last_name` varchar(25) NOT NULL,
    `email` varchar(100) NOT NULL,
    `phone` varchar(25) NOT NULL
    );

  ALTER TABLE `Attendee`
        ADD PRIMARY KEY (`id`);

    ALTER TABLE `Attendee`
        MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

-- ----------------------------
-- EVENT TABLE
DROP TABLE IF EXISTS `Event`;

CREATE TABLE IF NOT EXISTS `Event` (
    `id` int(11) NOT NULL,
    `event_name` varchar(100) NOT NULL,
    `artist` varchar(100) NOT NULL,
    `event_date` varchar(25) NOT NULL,
    `venue` varchar(100) NOT NULL,
    `capacity` int(11) NOT NULL
);

ALTER TABLE `Event`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `Event`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

-- ----------------------------
-- TICKET_XREF TABLE
DROP TABLE IF EXISTS `ticket_xref`;

CREATE TABLE IF NOT EXISTS `ticket_xref` (
    `id` int(11) NOT NULL,
    `attendee_id` int(11) NOT NULL,
    `event_id` int(11) NOT NULL,
    `ticket_id` varchar(20) NOT NULL,
    `confirmation_code` varchar(20) NOT NULL,
    `seat_number` varchar(10) NOT NULL,
    `purchase_date` varchar(25) NOT NULL
);

ALTER TABLE `ticket_xref`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `ticket_xref`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `ticket_xref`
  ADD KEY `ticket_xref_ibfk_1` (`attendee_id`),
  ADD KEY `ticket_xref_ibfk_2` (`event_id`);

ALTER TABLE `ticket_xref`
  ADD CONSTRAINT `ticket_xref_ibfk_1`
  FOREIGN KEY (`attendee_id`) REFERENCES `Attendee` (`id`)
  ON DELETE CASCADE
  ON UPDATE CASCADE;

ALTER TABLE `ticket_xref`
  ADD CONSTRAINT `ticket_xref_ibfk_2`
  FOREIGN KEY (`event_id`) REFERENCES `Event` (`id`)
  ON UPDATE CASCADE;

  SET FOREIGN_KEY_CHECKS=1;