import sqlite3
import click
from dataclasses import dataclass
import datetime
import dropbox
import initialize


# Click uses its own echo function. It's importants only if using ASCII colors

connector = sqlite3.connect("contact_book.db")


@dataclass
class Contact:
    """ The class is used to customize the string representation of the contact """

    name: str
    surname: str
    phone: str
    email: str = None
    # age: int = None
    birthday: str = None

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

        if self.birthday:
            # The string from SQLite has to be reformatted as a datetime object
            bday = [
                int(date_element)
                for date_element in self.birthday.split()[0].split("-")
            ]

            print(bday)

            bday = datetime.date(*bday)
            fields.append(f"Birthday: {bday.day}-{bday.month}-{bday.year}")

            age = (datetime.date.today() - bday).days // 365
            fields.append(f"Age: {age}")

        fields += ["=" * delim_rep]

        return "\n".join(fields)


@click.group()
def cli():
    pass


@cli.command()
@click.option("-t", "--token", default=None, type=click.STRING)
def backup(token):
    """Create a backup with Dropbox"""

    if token:
        access_token = token
    else:
        with open("access_token") as token:
            access_token = token.readline()

    dbx = dropbox.Dropbox(access_token)
    with open("contact_book.db", "rb") as f:
        dbx.files_upload(
            f.read(), "/Apps/contact_cli.db", mode=dropbox.files.WriteMode("overwrite")
        )


@cli.command()
def reset():
    """Reset the database. Caution: all your contact will be lost!"""
    if click.confirm(
        "Do you want to reset the contact book? All contacts will be lost!"
    ):
        initialize.reset(connector)


@cli.command()
@click.argument("name", type=click.STRING)
@click.argument("surname", type=click.STRING)
@click.argument("phone", type=click.STRING)
@click.option("-e", "--email", default=None, type=click.STRING)
@click.option(
    "-b",
    "--birthday",
    default=None,
    type=click.DateTime(formats=["%d-%m-%Y"]),
    help="dd-mm-yyyy",
)
def new(name, surname, phone, email, birthday):
    """Create a new entry in the contact book, if it does not already exist"""

    # Interrupt if entry exists
    if contains(name, surname):
        print(f"There is already an entry for {name} {surname}")
        return

    insert = """
        INSERT INTO contacts
        VALUES (?, ?, ?, ?, ?)
        """

    contact = (name.capitalize(), surname.capitalize(), phone, email, birthday)

    connector.execute(insert, contact)
    connector.commit()

    if birthday:
        # Format birthday as a string for __str__ method of Contact
        contact = (*contact[:-1], str(birthday))
    else:
        # Here birthday is None
        contact = (*contact[:-1], birthday)

    print(f"You added: {Contact(*contact)} ")


@cli.command()
@click.option("-a", "--all", is_flag=True, help="Show all the columns in the table")
@click.option("-n", "--name", default=None, type=click.STRING)
@click.option("-s", "--surname", default=None, type=click.STRING)
@click.option(
    "-f", "--find", is_flag=True, help="Do only partial matching of name or surname"
)
def show(all, name, surname, find):
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

    # If flag --find is passed to partial matching
    if find:
        command = command.replace("=", "LIKE")

        # Add wildcards to the arguments
        arguments = ["%" + argument + "%" for argument in arguments]

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
@click.option("-p", "--phone", default=None, type=click.STRING)
@click.option("-e", "--email", default=None, type=click.STRING)
@click.option(
    "-b",
    "--birthday",
    default=None,
    type=click.DateTime(formats=["%d-%m-%Y"]),
    help="dd-mm-yyyy",
)
def update(name, surname, phone, email, birthday):
    """Update the phone number, or email of a person"""

    name = name.capitalize()
    surname = surname.capitalize()

    if phone is None and email is None and birthday is None:
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

    if birthday:
        command += "birthday = ?,"
        arguments.append(birthday)

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

    connector.execute(
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
