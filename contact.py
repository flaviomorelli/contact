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
def show(all):
    """Show contacts in the database"""
    columns = "name, surname, phone"
    if all:
        columns = "*"
    cursor = connector.execute(
        f"""
        SELECT {columns} FROM contacts
        ORDER BY surname
        """
    )

    for row in cursor:
        print(Contact(*row))
        # print(f"{row[1]}, {row[0]}: {row[2]}")


@cli.command()
@click.argument("name", type=click.STRING)
@click.argument("surname", type=click.STRING)
def delete(name, surname):
    name, surname = name.capitalize(), surname.capitalize()

    if not contains(name, surname):
        print(f"{name} {surname} could not be found.")
        return

    result = connector.execute(
        """
        DELETE  FROM contacts
        WHERE name=? AND surname=?""",
        (name, surname),
    )
    connector.commit()

    print(f"{result.arraysize} contacts were deleted")


#    result = connector.commit()

# print(f"{list(cur)}")

# print(list(query))

# if list(query) == []:
# print("There is no such entry")

#    else:
#       print(f"{name} {surname} was deleted.")


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


# add_contact(connector, "Karl", "Marx", "089123445", "karl.marx@posteo.de", 40)
# add_contact(connector, "Groucho", "Marx", "8947529835", "groucho.marx@posteo.de")
# add_contact(connector, "Friedrich", "Engels", "838575729")
