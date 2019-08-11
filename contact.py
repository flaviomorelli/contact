import sqlite3
import click

# Click uses its own echo function. It's importants only if using ASCII colors

connector = sqlite3.connect("contact_book.db")


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
    insert = """
        INSERT INTO contacts
        VALUES (?, ?, ?, ?, ?)
        """

    contact = (name, surname, phone, email, age)

    connector.execute(insert, contact)
    connector.commit()
    print(f"You added {contact} to your contacts")


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
        print(row)
        # print(f"{row[1]}, {row[0]}: {row[2]}")


# setup_db(connector)

# add_contact(connector, "Karl", "Marx", "089123445", "karl.marx@posteo.de", 40)
# add_contact(connector, "Groucho", "Marx", "8947529835", "groucho.marx@posteo.de")
# add_contact(connector, "Friedrich", "Engels", "838575729")

# show_all_contacts(connector)

# connector.execute(
#     """
#     INSERT INTO contacts
#     VALUES (?, ?, ?, ?, ?)
#     """,
#     karl_marx,
# )
# It is necessary to commit after each insert!
# connector.commit()

if __name__ == "main":
    reset()
