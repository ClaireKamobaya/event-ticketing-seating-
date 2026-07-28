"""Defines the MySQLPersistenceWrapper class."""
from event_ticketing.application_base import ApplicationBase
from mysql import connector
from mysql.connector.pooling import (MySQLConnectionPool)
import inspect
import json


class MySQLPersistenceWrapper(ApplicationBase):
    """Implements the MySQLPersistenceWrapper class."""

    def __init__(self, config: dict) -> None:
        """Initializes object."""
        self._config_dict = config
        self.META = config["meta"]
        self.DATABASE = config["database"]
        super().__init__(subclass_name=self.__class__.__name__,
                          logfile_prefix_name=self.META["log_prefix"])
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}:It works!')

        # Database Configuration Constants
        self.DB_CONFIG = {}
        self.DB_CONFIG['database'] = \
            self.DATABASE["connection"]["config"]["database"]
        self.DB_CONFIG['user'] = self.DATABASE["connection"]["config"]["user"]
        self.DB_CONFIG['host'] = self.DATABASE["connection"]["config"]["host"]
        self.DB_CONFIG['port'] = self.DATABASE["connection"]["config"]["port"]
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: DB Connection Config Dict: {self.DB_CONFIG}')

        # Database Connection
        self._connection_pool = \
            self._initialize_database_connection_pool(self.DB_CONFIG)

        # SQL String Constants
        self.SELECT_ALL_EVENTS = \
            "SELECT id, event_name, artist, event_date, venue, capacity FROM Event"

        self.SELECT_ALL_ATTENDEES = \
            "SELECT id, registration_id, first_name, last_name, email, phone FROM Attendee"

        self.INSERT_ATTENDEE = \
            "INSERT INTO Attendee (registration_id, first_name, last_name, email, phone) " \
            "VALUES (%s, %s, %s, %s, %s)"

        self.INSERT_TICKET = \
            "INSERT INTO ticket_xref (attendee_id, event_id, ticket_id, confirmation_code, seat_number, purchase_date) " \
            "VALUES (%s, %s, %s, %s, %s, %s)"

        self.SELECT_TICKETS_BY_ATTENDEE = \
            "SELECT t.id, e.event_name, t.seat_number, t.confirmation_code, t.purchase_date " \
            "FROM ticket_xref t JOIN Event e ON t.event_id = e.id " \
            "WHERE t.attendee_id = %s"

        self.UPDATE_ATTENDEE = \
            "UPDATE Attendee SET email = %s, phone = %s WHERE id = %s"

        self.DELETE_TICKET = \
            "DELETE FROM ticket_xref WHERE id = %s"

    ##### Private Utility Methods #####

    def _initialize_database_connection_pool(self, config: dict) -> MySQLConnectionPool:
        """Initializes database connection pool."""
        try:
            self._logger.log_debug(f'Creating connection pool...')
            cnx_pool = \
                MySQLConnectionPool(pool_name=self.DATABASE["pool"]["name"],
                                     pool_size=self.DATABASE["pool"]["size"],
                                     pool_reset_session=self.DATABASE["pool"]["reset_session"],
                                     use_pure=self.DATABASE["pool"]["use_pure"],
                                     **config)
            self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Connection pool successfully created!')
            return cnx_pool
        except connector.Error as err:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem creating connection pool: {err}')
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Check DB cnfg:\n{json.dumps(self.DATABASE)}')
        except Exception as e:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:Problem creating connection pool: {e}')
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:Check DB conf:\n{json.dumps(self.DATABASE)}')

    ##### Public Data Access Methods #####

    def select_all_events(self) -> list:
        """Returns a list of all event rows."""
        cnx = self._connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(self.SELECT_ALL_EVENTS)
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()
        return rows

    def select_all_attendees(self) -> list:
        """Returns a list of all attendee rows."""
        cnx = self._connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(self.SELECT_ALL_ATTENDEES)
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()
        return rows

    def insert_attendee(self, registration_id: str, first_name: str,
                         last_name: str, email: str, phone: str) -> int:
        """Inserts a new attendee and returns the new attendee's id."""
        cnx = self._connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute(self.INSERT_ATTENDEE,
                        (registration_id, first_name, last_name, email, phone))
        cnx.commit()
        new_id = cursor.lastrowid
        cursor.close()
        cnx.close()
        return new_id

    def insert_ticket(self, attendee_id: int, event_id: int, ticket_id: str,
                       confirmation_code: str, seat_number: str, purchase_date: str) -> int:
        """Inserts a new ticket and returns the new ticket's id."""
        cnx = self._connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute(self.INSERT_TICKET,
                        (attendee_id, event_id, ticket_id, confirmation_code, seat_number, purchase_date))
        cnx.commit()
        new_id = cursor.lastrowid
        cursor.close()
        cnx.close()
        return new_id

    def select_tickets_by_attendee(self, attendee_id: int) -> list:
        """Returns all tickets belonging to a given attendee."""
        cnx = self._connection_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(self.SELECT_TICKETS_BY_ATTENDEE, (attendee_id,))
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()
        return rows

    def update_attendee(self, attendee_id: int, email: str, phone: str) -> bool:
        """Updates an attendee's email and phone number."""
        cnx = self._connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute(self.UPDATE_ATTENDEE, (email, phone, attendee_id))
        cnx.commit()
        success = cursor.rowcount > 0
        cursor.close()
        cnx.close()
        return success

    def delete_ticket(self, ticket_id: int) -> bool:
        """Deletes a ticket by its id."""
        cnx = self._connection_pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute(self.DELETE_TICKET, (ticket_id,))
        cnx.commit()
        success = cursor.rowcount > 0
        cursor.close()
        cnx.close()
        return success