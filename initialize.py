import sqlite3
import click
import faker
import random
import datetime
import sys

"""This module inizializes the database with fake data"""

connector = sqlite3.connect("contact_book.db")
fake = faker.Faker()
n_contacts = 30

def reset(connector):
    """Reset the database. Caution: all your contact will be lost!"""
    connector.executescript(
        """
        DROP TABLE IF EXISTS contacts;

        CREATE TABLE contacts(
        NAME         TEXT            NOT NULL,
        SURNAME      TEXT            NOT NULL,
        PHONE        TEXT            NOT NULL,
        EMAIL        TEXT,       
        BIRTHDAY     TEXT
        );
        """
    )

    print("The contact book has been reset")

def mock_database(connector, n_contacts):
    for _ in range(n_contacts):
        name = fake.first_name()
        surname = fake.last_name()
        email = f"{name.lower()}.{surname.lower()}@{fake.free_email_domain()}"
        phone = fake.msisdn()
        # birthday has to be cast into a string to mimick what click.DateTime 
        # does in contact new in the main script
        birthday = str(fake.date_between(start_date="-80y", end_date="-15y"))

        connector.execute(
            """
            INSERT INTO contacts
            VALUES (?, ?, ?, ?, ?)""",
            (name, surname, phone, email, birthday),
        )

        connector.commit()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        n_contacts = int(sys.argv[1])

    reset(connector)
    mock_database(connector, n_contacts)