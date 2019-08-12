import sqlite3
import click
from dataclasses import dataclass

# Click uses its own echo function. It's importants only if using ASCII colors

connector = sqlite3.connect("contact_book.db")


@dataclass
class Contact:
    """ The class is used to customize the string representation of the contact """

    name: str
    surname: str
    phone: str
    email: str = None
    age: int = None

    def __str__(self):
        delim_rep = 20

        fields = [
            "",
            "=" * delim_rep,
            f"{self.name} {self.surname.upper()}",
            self.phone,
        ]

        if self.email:
            fields.append(self.email)

        if self.age:
            fields.append(f"Age: {self.age} years")

        fields += ["=" * delim_rep]

        return "\n".join(fields)


@click.group()
def cli():
    pass


@cli.command()
def reset():
    """Reset the database. Caution: all your contact will be lost!"""
    if click.confirm(
        "Do you want to reset the contact book? All contacts will be lost!"
    ):

        connector.executescript(
            """
            DROP TABLE IF EXISTS contacts;

            CREATE TABLE contacts(
            NAME         TEXT            NOT NULL,
            SURNAME      TEXT            NOT NULL,
            PHONE        TEXT            NOT NULL,
            EMAIL        TEXT,       
            AGE          INT
            );
            """
        )

        print("The contact book has been reset")


@cli.command()
@click.argument("name", type=click.STRING)
@click.argument("surname", type=click.STRING)
@click.argument("phone", type=click.STRING)
@click.option("--email", default=None, type=click.STRING)
@click.option("--age", default=None, type=click.INT)
def new(name, surname, phone, email, age):
    """Create a new entry in the contact book, if it does not already exists"""

    # Interrupt if entry exists
    if contains(name, surname):
        print(f"There is already an entry for {name} {surname}")
        return

    insert = """
        INSERT INTO contacts
        VALUES (?, ?, ?, ?, ?)
        """

    contact = (name.capitalize(), surname.capitalize(), phone, email, age)

    connector.execute(insert, contact)
    connector.commit()
    print(f"You added: {Contact(*contact)} ")


@cli.command()
@click.option("--all", is_flag=True, help="Show all the columns in the table")
@click.option("--name", default=None, type=click.STRING)
@click.option("--surname", default=None, type=click.STRING)
def show(all, name, surname):
    """Show contacts in the database. By default, only name and surname are shown"""

    columns = "name, surname, phone"

    if all:
        columns = "*"

    # Note that the user is not able to inject {column} in the f-string
    command = f"SELECT {columns} FROM contacts"
    arguments = []

    # If any flagged is passed include a where statement
    if name or surname:
        command += " WHERE"

    condition = []

    if name:
        condition.append(" name = ?")
        name = name.capitalize()
        arguments.append(name)

    if surname:
        condition.append(" surname = ?")
        surname = surname.capitalize()
        arguments.append(surname)

    # If name and surname are passed join with AND
    if name and surname:
        command += " AND".join(condition)
    elif not condition == []:
        command += condition[0]

    command = command + " ORDER BY surname"

    cursor = connector.execute(command, tuple(arguments))

    n_contacts = 0
    for row in cursor:
        n_contacts += 1
        print(Contact(*row))

    print(f"\nReturned {n_contacts} contacts\n")


@cli.command()
@click.argument("name", type=click.STRING)
@click.argument("surname", type=click.STRING)
@click.option("--phone", default=None, type=click.STRING)
@click.option("--email", default=None, type=click.STRING)
def update(name, surname, phone, email):
    """Update the phone number, or email of a person"""

    name = name.capitalize()
    surname = surname.capitalize()

    if phone is None and email is None:
        print("Use the --phone and --email flags to update contact information.")
        return

    if not contains(name, surname):
        print("{name} {surname} was not found in the contact book.")
        return

    command = "UPDATE contacts SET "
    arguments = []

    if phone:
        command += "phone = ?,"
        arguments.append(phone)

    if email:
        command += "email = ?,"
        arguments.append(email)

    # Eliminate the extra comma from the command
    command = command[:-1]
    command += " WHERE name = ? AND surname = ?"

    arguments += [name, surname]
    arguments = tuple(arguments)

    result = connector.execute(command, arguments)
    connector.commit()

    print(f"Number of contacts updated: {result.arraysize}")


@cli.command()
@click.argument("name", type=click.STRING)
@click.argument("surname", type=click.STRING)
def delete(name, surname):
    """Delete a person from the contact book 
    with a given name and surname"""
    name, surname = name.capitalize(), surname.capitalize()

    if not contains(name, surname):
        print("No matching contacts found. No contacts were delted")
        return

    result = connector.execute(
        """
        DELETE  FROM contacts
        WHERE name=? AND surname=?""",
        (name, surname),
    )
    connector.commit()

    print(f"{name} {surname} was deleted from the contact book")


def contains(name, surname):
    """Check if the entry already exists in the contacts table"""
    query = connector.execute(
        """
        SELECT * FROM contacts
        WHERE name=? AND surname=?""",
        (name.capitalize(), surname.capitalize()),
    )

    if list(query) == []:
        return False

    return True
