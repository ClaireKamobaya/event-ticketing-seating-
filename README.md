# Event Ticketing and Seating

This is my final project for IT566. It's a Python app that connects to a MySQL database and lets you manage event tickets — register attendees, look at events, and book tickets.

## What it does

- Shows all events and attendees
- Registers new attendees (auto-generates a registration ID)
- Books tickets and auto-generates a ticket ID + confirmation code
- Lets you look up tickets for a specific attendee
- Won't crash if you type in a bad ID — just shows an error message instead

## How it's built

I followed the layered architecture from the textbook:

- **Persistence layer** — talks directly to the database (runs the actual SQL queries)
- **Service layer** — the logic in between, like generating ticket IDs and confirmation codes
- **Presentation layer** — the menu you actually see and type into

## Database

Three tables: `Attendee`, `Event`, and `ticket_xref`. The xref table is what connects the other two — since one attendee can book tickets to multiple events, and one event can have lots of attendees, you need that middle table to link them (many-to-many relationship). It also has the foreign keys set up so you can't book a ticket for an attendee or event that doesn't actually exist.

## How to run it

1. Install the dependencies:
```bash
pipenv --python 3.12
pipenv install
```

2. Set up the database (MAMP needs to be running first):
```bash
cd database
./initialize_database.sh
```
This drops and rebuilds the database from scratch, makes a dedicated database user (not root), builds the tables, and loads some test data.

3. Run the app:
```bash
pipenv run python src/main.py -c config/event_ticketing_app_config.json
```

## Database scripts

Everything's in the `database/` folder:
- `drop_database.sql` / `create_database.sql`
- `drop_user.sql` / `create_user.sql`
- `create_tables.sql`
- `initialize_test_data.sql`
- `initialize_database.sh` — runs everything above in the right order

## Owner

Claire Kamobaya — IT566, Marymount University