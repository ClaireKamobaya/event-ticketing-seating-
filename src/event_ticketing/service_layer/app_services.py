"""Implements AppServices Class."""
from event_ticketing.application_base import ApplicationBase
from event_ticketing.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
import inspect
import uuid
import datetime


class AppServices(ApplicationBase):
    """AppServices Class Definition."""

    def __init__(self, config: dict) -> None:
        """Initializes object."""
        self._config_dict = config
        self.META = config["meta"]
        super().__init__(subclass_name=self.__class__.__name__,
                          logfile_prefix_name=self.META["log_prefix"])
        self.DB = MySQLPersistenceWrapper(config)
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}:It works!')

    def get_all_events(self) -> list:
        """Returns a list of all events."""
        return self.DB.select_all_events()

    def get_all_attendees(self) -> list:
        """Returns a list of all attendees."""
        return self.DB.select_all_attendees()

    def register_attendee(self, first_name: str, last_name: str,
                           email: str, phone: str) -> int:
        """Registers a new attendee with an auto-generated registration_id."""
        registration_id = f"REG{uuid.uuid4().hex[:8].upper()}"
        new_id = self.DB.insert_attendee(registration_id, first_name, last_name, email, phone)
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Registered attendee {new_id} with registration_id {registration_id}')
        return new_id

    def book_ticket(self, attendee_id: int, event_id: int, seat_number: str) -> dict:
        """Books a ticket for an attendee at a given event, returns confirmation details."""
        ticket_id = f"TICK{uuid.uuid4().hex[:8].upper()}"
        confirmation_code = f"CONF{uuid.uuid4().hex[:8].upper()}"
        purchase_date = datetime.date.today().isoformat()

        new_id = self.DB.insert_ticket(attendee_id, event_id, ticket_id,
                                        confirmation_code, seat_number, purchase_date)

        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Booked ticket {ticket_id} for attendee {attendee_id}')

        return {
            "ticket_id": ticket_id,
            "confirmation_code": confirmation_code,
            "seat_number": seat_number,
            "purchase_date": purchase_date
        }

    def get_attendee_tickets(self, attendee_id: int) -> list:
        """Returns all tickets belonging to a given attendee."""
        return self.DB.select_tickets_by_attendee(attendee_id)