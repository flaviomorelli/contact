import sqlite3
import click
import faker
import random
import datetime

"""This module inizializes the database with fake data"""

connector = sqlite3.connect("contact_book.db")
fake = faker.Faker()
n_contacts = 30

for _ in range(n_contacts):
    name = fake.first_name()
    surname = fake.last_name()
    email = f"{name}.{surname}@{fake.free_email_domain()}"
    phone = fake.msisdn()
    age = random.randint(15, 70)

    connector.execute(
        """
        INSERT INTO contacts
        VALUES (?, ?, ?, ?, ?)""",
        (name, surname, phone, email, age),
    )

    connector.commit()
