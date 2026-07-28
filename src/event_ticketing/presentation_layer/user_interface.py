"""Implements the application user interface."""
from event_ticketing.application_base import ApplicationBase
from event_ticketing.service_layer.app_services import AppServices
import inspect


class UserInterface(ApplicationBase):
    """UserInterface Class Definition."""

    def __init__(self, config: dict) -> None:
        """Initializes object."""
        self._config_dict = config
        self.META = config["meta"]
        super().__init__(subclass_name=self.__class__.__name__,
                          logfile_prefix_name=self.META["log_prefix"])
        self.DB = AppServices(config)
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}:It works!')

    def start(self):
        """Start main user interface."""
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: User interface started!')
        self._show_menu()

    def _show_menu(self):
        """Displays the main menu loop."""
        while True:
            print("\n===== Event Ticketing and Seating =====")
            print("1. View all events")
            print("2. View all attendees")
            print("3. Register a new attendee")
            print("4. Book a ticket")
            print("5. View my tickets")
            print("6. Update my contact info")
            print("7. Cancel a ticket")
            print("8. Exit")
            choice = input("Enter your choice (1-8): ")

            if choice == "1":
                self._view_events()
            elif choice == "2":
                self._view_attendees()
            elif choice == "3":
                self._register_attendee()
            elif choice == "4":
                self._book_ticket()
            elif choice == "5":
                self._view_my_tickets()
            elif choice == "6":
                self._update_contact()
            elif choice == "7":
                self._cancel_ticket()
            elif choice == "8":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please try again.")

    def _view_events(self):
        events = self.DB.get_all_events()
        print("\n--- Events ---")
        for e in events:
            print(f"ID: {e['id']} | {e['event_name']} - {e['artist']} on {e['event_date']} "
                  f"at {e['venue']} (Capacity: {e['capacity']})")

    def _view_attendees(self):
        attendees = self.DB.get_all_attendees()
        print("\n--- Attendees ---")
        for a in attendees:
            print(f"ID: {a['id']} | {a['first_name']} {a['last_name']} ({a['email']})")

    def _register_attendee(self):
        first_name = input("First name: ")
        last_name = input("Last name: ")
        email = input("Email: ")
        phone = input("Phone: ")
        new_id = self.DB.register_attendee(first_name, last_name, email, phone)
        print(f"Registered! Your attendee ID is: {new_id}")

    def _book_ticket(self):
        attendee_id = input("Your attendee ID: ")
        event_id = input("Event ID: ")
        seat_number = input("Seat number (e.g., A12): ")
        try:
            result = self.DB.book_ticket(int(attendee_id), int(event_id), seat_number)
            print(f"Ticket booked! Confirmation code: {result['confirmation_code']}, "
                  f"Ticket ID: {result['ticket_id']}")
        except ValueError:
            print("Error: Attendee ID and Event ID must be numbers.")
        except Exception as e:
            print("Error: Could not book ticket. Please check that the Attendee ID "
                  "and Event ID both exist (use options 1 and 2 to check).")
            self._logger.log_error(f'_book_ticket: {e}')

    def _view_my_tickets(self):
        attendee_id = input("Your attendee ID: ")
        try:
            tickets = self.DB.get_attendee_tickets(int(attendee_id))
            print("\n--- Your Tickets ---")
            if not tickets:
                print("No tickets found for this attendee.")
            for t in tickets:
                print(f"Ticket ID: {t['id']} | {t['event_name']} | Seat: {t['seat_number']} | "
                      f"Confirmation: {t['confirmation_code']} | Purchased: {t['purchase_date']}")
        except ValueError:
            print("Error: Attendee ID must be a number.")
        except Exception as e:
            print("Error: Could not retrieve tickets.")
            self._logger.log_error(f'_view_my_tickets: {e}')

    def _update_contact(self):
        attendee_id = input("Your attendee ID: ")
        email = input("New email: ")
        phone = input("New phone: ")
        try:
            success = self.DB.update_attendee_contact(int(attendee_id), email, phone)
            if success:
                print("Contact info updated!")
            else:
                print("No attendee found with that ID.")
        except ValueError:
            print("Error: Attendee ID must be a number.")
        except Exception as e:
            print("Error: Could not update contact info.")
            self._logger.log_error(f'_update_contact: {e}')

    def _cancel_ticket(self):
        ticket_id = input("Ticket ID to cancel (use option 5 to find it): ")
        try:
            success = self.DB.cancel_ticket(int(ticket_id))
            if success:
                print("Ticket cancelled!")
            else:
                print("No ticket found with that ID.")
        except ValueError:
            print("Error: Ticket ID must be a number.")
        except Exception as e:
            print("Error: Could not cancel ticket.")
            self._logger.log_error(f'_cancel_ticket: {e}')